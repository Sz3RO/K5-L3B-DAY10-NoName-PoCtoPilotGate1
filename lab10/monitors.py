"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def peak_hour_review_load(trials):
    """Vận hành: số ca vào hàng chờ người duyệt (chuyển người + kiểm lại) trong 60 phút đông nhất của một ngày,
    lấy ngày tệ nhất. So với sức duyệt (review_capacity_per_hour × người trực) để biết khi nào phải gọi thêm người."""
    days = {}
    for t in trials:
        if t.get("review_kind") and t.get("arrive_min") is not None:
            days.setdefault((t["seed"], t.get("day")), []).append(t["arrive_min"])
    worst = 0
    for mins in days.values():
        mins.sort()
        j = 0
        for i, m in enumerate(mins):
            while mins[j] <= m - 60:
                j += 1
            worst = max(worst, i - j + 1)
    return worst


def llm_fail_open_rate(trials):
    """Kỹ thuật: tỉ lệ ticket mà bước LLM lỗi (429...) và trợ lý chạy tiếp theo kiểu fail_open, tức là
    quyết định chỉ còn dựa vào cổng chặn trong guards.py."""
    hit = sum(any(e.get("type") == "llm_fallback" and e.get("mode") == "fail_open" for e in t["events"]) for t in trials)
    return hit / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "peak_hour_review_load": peak_hour_review_load,
    "llm_fail_open_rate": llm_fail_open_rate,
}
STARTER_MONITORS = ("escalation_rate",)
