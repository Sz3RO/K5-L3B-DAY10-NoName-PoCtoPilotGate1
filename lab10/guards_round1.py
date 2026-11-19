"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
CỔNG CỦA BÀN NoName (vòng 1). Nguyên tắc chung: mọi cổng chỉ đọc NGUỒN SỰ THẬT (tracking DB, bảng chính sách theo ngày
hiệu lực, bảng phê duyệt, sổ cái, ops_limits); KHÔNG đọc chữ khách viết và KHÔNG xử lý riêng theo mã ticket / mã đơn.

  G0  pre_guard            ghim phiên bản chính sách theo NGÀY HIỆU LỰC (không tin cờ index_active).    ← HAZOP INVALID
  G1  issue_refund         số tiền ≤ quyền lợi tính từ tracking DB + chính sách hiệu lực; quyền lợi = 0 thì từ chối;
                           người trả luôn là LOGIX nếu không có phê duyệt.                               ← pre-mortem Kỹ thuật,
                                                                                                           HAZOP WRONG / PERTURBED
  G2  issue_refund         không hoàn trùng: đơn đã có dòng trong sổ cái thì từ chối (chặn cả ghi lặp
                           khi LLM xác nhận lỗi 429).                                                    ← pre-mortem Kinh doanh
  G3  issue_refund         vượt hạn mức tự động thì phải có phê duyệt HỢP LỆ (đúng ticket, còn hạn,
                           status valid, đủ max_vnd), nếu không chuyển người duyệt; hãng đã chạm trần
                           lỗi/ngày thì chuyển người TRƯỚC khi ghi tiền.                                 ← pre-mortem Con người & vận hành
  G4  file_carrier_fault   chỉ ghi lỗi khi tracking có độ trễ đủ và nguyên nhân thuộc fault_causes;
                           ghi đúng kiện trễ / đúng hãng / đúng tài xế / đúng số ngày theo DB.           ← pre-mortem Pháp lý
  G5  notify_carrier       chỉ gửi các trường chính sách cho phép (carrier_notice_fields): không gửi
                           tên, SĐT người nhận, không chép nguyên chữ khách gõ.                          ← HAZOP ngoài kỹ thuật (bên thứ ba)
  G6  send_reply           số tiền báo khách = đúng số đã ghi sổ cái cho ticket này.
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


# ───────────────────────────── tra cứu nguồn sự thật (chỉ đọc) ─────────────────────────────

def _policy(ctx):
    """Chính sách có hiệu lực vào ngày hôm nay (theo effective_from / effective_to), không theo cờ index_active."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """(đơn, kiện của ticket, độ trễ theo tracking DB, chính sách hiệu lực). Thiếu thứ gì thì trả None ở chỗ đó."""
    order = ctx.tools.lookup_order(order_id)
    if order is None:
        return None, None, 0, _policy(ctx)
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), _policy(ctx)


def _approval_ok(ctx, approval_id, order_id, amount):
    """Phê duyệt hợp lệ: có thật, đúng ticket, đúng đơn, status valid, chưa hết hạn, max_vnd đủ."""
    rows = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not rows:
        return False
    a = rows[0]
    return (a.get("ticket_id") == ctx.ticket.get("ticket_id") and a.get("order_id") == order_id
            and a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
            and a.get("max_vnd", 0) >= amount)


def _strikes_today(ctx, carrier_id):
    return len(ctx.tools.fault_rows(carrier_id=carrier_id))


def _strike_cap(ctx):
    return ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")


def _last(ctx, kind):
    return next((e for e in reversed(ctx.events) if e.get("type") == kind), {})


# ───────────────────────────── G0 · trước khi trợ lý đọc ticket ─────────────────────────────

def pre_guard(ctx):
    pol = _policy(ctx)
    if pol is None:
        return Verdict.escalate("không có chính sách hoàn tiền nào có hiệu lực hôm nay: chuyển người")
    if not pol.get("index_active"):
        ctx.log("policy_pinned", policy_id=pol["policy_id"], reason="cờ index_active lệch ngày hiệu lực")
    return Verdict.allow(policy_id=pol["policy_id"])


# ───────────────────────────── G1–G6 · trước mỗi lệnh ghi ─────────────────────────────

def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    if tool == "send_reply":
        return _gate_reply(ctx, action)
    return Verdict.allow()


def _gate_refund(ctx, action):
    order, parcel, delay, pol = _facts(ctx, action.get("order_id"))
    if order is None or pol is None:
        return Verdict.escalate("không đối chiếu được đơn hoặc chính sách: chuyển người")

    # G2 · không hoàn trùng (sổ cái là nguồn sự thật, cờ refund_status chỉ cập nhật theo lô đêm)
    if ctx.tools.ledger_rows(order_id=order["order_id"]):
        ctx.log("refund_blocked", gate="G2", why="đơn đã có khoản hoàn trong sổ cái")
        return Verdict.deny("đơn đã có khoản hoàn trong sổ cái: không hoàn trùng")

    # G1 · quyền lợi tính từ tracking DB + chính sách hiệu lực
    entitled = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    asked = int(action.get("amount_vnd") or 0)
    aid = action.get("approval_id")
    if entitled <= 0:
        ctx.log("refund_blocked", gate="G1", asked=asked, entitled=0, db_delay_days=delay)
        return Verdict.deny("theo tracking DB và chính sách hiệu lực, đơn chưa đủ điều kiện hoàn")
    changes = {}
    if asked > entitled:
        changes["amount_vnd"] = entitled
    if action.get("payer", "LOGIX") != "LOGIX" and not (aid and _approval_ok(ctx, aid, order["order_id"], asked)):
        changes["payer"] = "LOGIX"
    final = changes.get("amount_vnd", asked)

    # G3 · phê duyệt và trần vận hành
    if aid and not _approval_ok(ctx, aid, order["order_id"], final):
        ctx.log("refund_escalated", gate="G3", why="phê duyệt không hợp lệ", approval_id=aid)
        return Verdict.escalate("phê duyệt không hợp lệ cho ticket này (sai ticket, hết hạn, đã dùng hoặc không đủ hạn mức)")
    if final > pol["auto_limit_vnd"] and not aid:
        ctx.log("refund_escalated", gate="G3", why="vượt hạn mức tự động", amount=final, limit=pol["auto_limit_vnd"])
        return Verdict.escalate(f"khoản hoàn {final}đ vượt hạn mức tự động {pol['auto_limit_vnd']}đ, chưa có phê duyệt")
    cap = _strike_cap(ctx)
    will_fault = _last(ctx, "proposal").get("do_fault") and H.carrier_at_fault(pol, parcel, delay)
    if will_fault and cap is not None and _strikes_today(ctx, parcel["carrier_id"]) >= cap:
        ctx.log("refund_escalated", gate="G3", why="hãng đã chạm trần lỗi trong ngày", carrier_id=parcel["carrier_id"])
        return Verdict.escalate(f"hãng {parcel['carrier_id']} đã có {cap} lỗi hôm nay: lỗi tiếp theo cần người duyệt")

    if changes:
        ctx.log("refund_modified", gate="G1", asked=asked, entitled=entitled, changes=changes, db_delay_days=delay)
        return Verdict.modify("sửa theo quyền lợi tính từ tracking DB và chính sách hiệu lực", **changes)
    return Verdict.allow()


def _gate_fault(ctx, action):
    order, parcel, delay, pol = _facts(ctx, action.get("order_id"))
    if order is None or pol is None:
        return Verdict.deny("không đối chiếu được đơn hoặc chính sách: không ghi lỗi hãng")
    # G4 · chỉ ghi lỗi khi tracking DB có căn cứ
    if not H.carrier_at_fault(pol, parcel, delay):
        ctx.log("fault_blocked", gate="G4", parcel_id=parcel["parcel_id"], cause=parcel.get("delay_cause"),
                db_delay_days=delay)
        return Verdict.deny("tracking DB không có căn cứ lỗi hãng (độ trễ chưa đủ hoặc nguyên nhân không thuộc lỗi hãng)")
    cap = _strike_cap(ctx)
    if cap is not None and _strikes_today(ctx, parcel["carrier_id"]) >= cap:
        ctx.log("fault_blocked", gate="G4", why="trần lỗi mỗi hãng mỗi ngày", carrier_id=parcel["carrier_id"])
        return Verdict.deny("hãng đã chạm trần lỗi tự động trong ngày: để người duyệt ghi")
    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    changes = {k: v for k, v in want.items() if action.get(k) != v}
    if changes:
        ctx.log("fault_modified", gate="G4", changes=changes)
        return Verdict.modify("ghi lỗi đúng kiện trễ, đúng hãng, đúng số ngày theo tracking DB", **changes)
    return Verdict.allow()


def _gate_notify(ctx, action):
    # G5 · chỉ gửi các trường mà chính sách cho phép gửi cho hãng
    pol = _policy(ctx)
    allowed = set((pol or {}).get("carrier_notice_fields") or ["order_id", "parcel_id", "district", "delay_days"])
    blocked = set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
    payload = action.get("payload") or {}
    keep = {k: v for k, v in payload.items() if k in allowed and k not in blocked}
    if keep != payload:
        ctx.log("notify_trimmed", gate="G5", dropped=sorted(set(payload) - set(keep)))
        return Verdict.modify("chỉ gửi cho hãng các trường chính sách cho phép", payload=keep)
    return Verdict.allow()


def _gate_reply(ctx, action):
    # G6 · số tiền báo khách khớp sổ cái
    paid = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(ticket_id=ctx.ticket.get("ticket_id")))
    if int(action.get("amount_vnd") or 0) != paid:
        ctx.log("reply_fixed", gate="G6", said=action.get("amount_vnd"), ledger=paid)
        return Verdict.modify("số tiền báo khách phải khớp sổ cái", amount_vnd=paid)
    return Verdict.allow()
