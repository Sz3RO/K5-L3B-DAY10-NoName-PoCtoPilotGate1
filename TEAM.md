# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `NoName`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-NoName-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S4

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Vũ Văn Trường | 2A202603910 | Kỹ sư cổng | ✓ |
|   2 | Lê Huy Anh | 2A202603786 | Sản phẩm và kinh doanh |             |
|   3 | Trần Thị Nhài | 2A202603911 | Vận hành và pháp lý |             |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## VuVanTruong-2A202603910

### Phần việc phụ trách

Kỹ sư cổng + trưởng nhóm. Câu 2.1, 2.2, 2.6, 2.8 và vòng 2 phần code. Phiếu B mục B0, B2, B7.1, B7.3 (cùng Lê Huy Anh), B8 phần số liệu;
Phiếu C mục C0, C2, C6–C9 (vòng 2: G7, monitor, ticket@seed). File `lab10/guards.py`, `lab10/monitors.py`; chạy mọi lệnh ký / đo / chốt / nhận thẻ / gom bài và push các mốc.

### Đóng góp cụ thể

- Fork repo, đặt danh tính Git theo MSSV, điền bảng thành viên và các mục cá nhân; chạy lệnh ký tiêu chí (người đứng tên `signed_by`: Lê Huy Anh), commit và push (`7a3a5d1`), chạy `lab10.checkpoint` (hash `d41707a3`) và push mốc v1 (`4aeda6d`).
- Duyệt và kiểm `lab10/guards.py` (bản code do Claude soạn, xem mục Dùng AI): G0 ghim chính sách theo ngày hiệu lực; G1 tính quyền lợi từ tracking DB; G2 chặn hoàn trùng; G3 phê duyệt hợp lệ (đúng ticket, đúng đơn, `valid`, còn hạn, đủ `max_vnd`); G4 chỉ ghi lỗi hãng khi có nguyên nhân trong tracking và hãng chưa quá 2 lỗi/ngày; G5 không gửi PII người nhận; G6 số tiền trả lời khớp sổ cái. Kiểm bằng `base · after`: `T-002@55` từ hỏng (20.000đ, 1 lỗi VNX) về ĐẠT, không ca đúng nào bị hỏng (`pass_rate` 1,0 / `pass_k` 1,0).
- Chạy ba mốc `R-base-before-20261119-154359-cc4e33`, `R-base-after-20261119-154406-cc4e33`, `R-base-prepared-20261119-154928-cc4e33`, lệnh `gate`, trace `T-002@55`, và ba ticket ad-hoc cho B7.3 (O-1012, O-1026, O-1024); điền B0, B2, B7.1, B7.3.
- Vòng 2 (thẻ S4): commit `fca5b53` (Nhận thẻ S4); duyệt G7 trong `_gate_refund` (trần hoàn tự động trong ngày = min(trần bàn, ngân sách Finance trong `ops_limits`)) và hai monitor `peak_hour_review_load`, `llm_fail_open_rate`; chạy từng lần đổi MỘT thứ (Phiếu C mục C0) và grade `R-S4-grade-20261119-170557-5b35f2` (6/6 mục ✅).
- Giữ nguyên hai bản chốt vòng 1 (`guards_round1.py`, `operating_gates.round1.json`) và không sửa tiêu chí sau khi ký; chịu trách nhiệm giải thích G0–G7, hai monitor và các số trong report lúc demo.

**Dùng AI:** Tôi dùng Claude (Claude Code, trên máy của tôi) cho các việc sau:
- Đọc toàn bộ repo và code lab bị khoá (`agent.py`, `tools.py`, `eval.py`, `ops.py`, `gate.py`), giải thích luật, lập plan chia việc cho 3 người.
- Soạn code cổng G0–G6 trong `lab10/guards.py`. Cổng viết theo luật đọc từ nguồn sự thật (chính sách theo ngày hiệu lực, tracking, sổ cái, phê duyệt, `ops_limits`), không xử lý riêng theo mã ticket hay câu chữ.
- Soạn nháp `config/acceptance_criteria.json`, `config/operating_gates.json`, Phiếu A (A1–A5) và Phiếu B (B0–B8).
- Chạy các lệnh đo theo lệnh của tôi: `lab10.eval` (base, after, prepared), `lab10.gate`, `lab10.trace`, ba ticket ad-hoc. Điền số liệu và dòng trace vào B0, B1, B2, B7.1, B7.3, B8.
- Hai lần review độc lập bằng một agent khác của Claude (trước khi ký và trước khi commit v1). Sửa lỗ hổng logic trong `decision_rule` và `stop_condition` theo kết quả review.
- Vòng 2 (thẻ S4): soạn G7 và hai monitor, chạy eval/grade/trace, đề xuất cấu hình (thử 2 người trực rồi bỏ, thu hẹp bỏ kho DN), soạn nháp Phiếu C (C0–C12), ba dòng ở B7.6 đánh dấu [Vòng 2 · S4] và `submission.json` (decision_v2, three_lines); hai lần review độc lập nữa (sau khi sửa, trước khi nộp) và sửa theo kết quả; chạy `check_submission --collect`.
- Điền ô "PIC ký" ở B8 và C12 theo lệnh của tôi: tên Lê Huy Anh, ghi rõ tôi ký thay theo uỷ quyền của bạn ấy.

Phần do tôi quyết, Claude không tự làm:
- duyệt phạm vi việc;
- cho phép ký tiêu chí, commit và push (`7a3a5d1`);
- cho phép chạy `lab10.checkpoint` (`d41707a3`) và commit v1 (`4aeda6d`);
- cho phép commit nhận thẻ (`fca5b53`) và commit nộp bài cuối;
- duyệt các thay đổi vòng 2 và nội dung ô "PIC ký" (ký thay Lê Huy Anh theo uỷ quyền).

Tôi đọc lại cổng và các số trước khi duyệt, và chịu trách nhiệm giải thích chúng lúc demo. Exit ticket không dùng AI.

### Bằng chứng

- Commit: `7a3a5d1` (Sign acceptance criteria), `4aeda6d` (LAB 10: chốt cổng vòng 1, quyết định v1), `fca5b53` (Nhận thẻ S4), commit nộp bài cuối (vòng 2).
- Mã lần chạy: `runs/R-base-before-20261119-154359-cc4e33`, `runs/R-base-after-20261119-154406-cc4e33`, `runs/R-base-prepared-20261119-154928-cc4e33`.
- Phiếu B: B0 dòng 1–3, B2, B7.1, B7.3. Phiếu C: C0, C2, C6–C9; grade `R-S4-grade-20261119-170557-5b35f2`.

### Exit ticket

- Một điều học được: cổng cấp hệ thống nên đặt trước lệnh ghi và chỉ đọc nguồn sự thật (tracking DB, sổ cái, phê duyệt), vì chỉ sửa prompt/model không chặn được lỗi chìm như hoàn sai 20.000đ hay ghi oan cho hãng.
- Một điều còn chưa chắc: bộ thử hôm nay chỉ có 22 ticket mock; chưa biết cổng có giữ được tính chất với đơn nhiều kiện, chính sách đổi ngày hiệu lực, và bài kiểm tra ẩn với cách viết ticket khác hay không.

## LeHuyAnh-2A202603786

### Phần việc phụ trách

Sản phẩm và kinh doanh. Câu 1.1, 1.5, 1.6, 2.3, 2.9, quyết định v1/v2. Phiếu A mục A1, A3, A4 (cùng Trần Thị Nhài), A5 (người đứng tên
`signed_by`); Phiếu B mục B1, B3, B7.4, B8 (cột v1); Phiếu C mục C7 (phần `business`), C12. File `config/acceptance_criteria.json`,
`config/operating_gates.json` mục `business`.

### Đóng góp cụ thể

- Duyệt và đứng tên người ký Bản tiêu chí (`config/acceptance_criteria.json`, `signed_by` Lê Huy Anh; lệnh ký chạy trên máy trưởng nhóm lúc 15:43:04, commit `7a3a5d1`): 5 ngưỡng bắt buộc (`pass_rate` 0,97, `pass_k` 0,95, ba chỉ số an toàn = 0), `escalation_rate` 0,25, `business_ops` (`cost_per_ticket` 6.000đ, `roi_min` 0,5, `queue_stuck` 0), `stop_condition` và bốn dòng `decision_rule`.
- Duyệt cổng kinh doanh (`config/operating_gates.json` mục `business`): trần hoàn tự động 1.000.000đ (một nửa ngân sách Finance 2.000.000đ), ngân sách chi phí 1.500đ/ticket, `pilot_scope` all 100%, `roi_min` 0,5; mỗi số có lý do từ `ops_limits`/`ops_facts`.
- Duyệt, chỉnh và chịu trách nhiệm Phiếu A A1 (mục tiêu cấp hệ thống), A3 (đọc khoảng tin cậy), A4 (câu "Nếu … thì …", soát bốn câu hỏi, ranh giới đầu ra); Phiếu B B1 (tự chặn hay người duyệt), B3 (bản đồ dữ liệu và drift REFUND-v3 → v4), B7.4, B8 cột v1.
- Soát ngưỡng với `data/world.json`, đọc lại tiêu chí trước khi ký; đồng ý quyết định v1 "Tiếp tục" dựa trên `R-base-prepared-20261119-154928-cc4e33` (pass_rate 1,0, pass_k 1,0, hoàn sai 0đ, ROI 1,24, chi phí 4.456đ/ticket).

**Dùng AI:** Bản nháp các phần của vai tôi được Claude (Claude Code) soạn trong phiên làm việc của trưởng nhóm Vũ Văn Trường:
- `config/acceptance_criteria.json`: ngưỡng, `stop_condition`, `decision_rule`.
- Phiếu A: các câu "Nếu … thì …", soát bốn câu hỏi, lý do ngưỡng `business_ops`.
- Phiếu B: B1 (ưu và nhược điểm của cổng tự chặn), B3 (bản đồ dữ liệu), B7.4 (lý do các số `business`), B8 (cột v1).
- Phiếu C: C7 (phần phạm vi `business.pilot_scope`), C12 (quyết định v2 "Thu hẹp" và ba dòng bắt buộc).

Tôi đã đọc lại tiêu chí trước khi tiêu chí được ký đứng tên tôi (`signed_by`), đối chiếu các ngưỡng với `data/world.json` (`ops_facts`, `ops_limits`), và đồng ý với quyết định v1 "Tiếp tục" dựa trên `R-base-prepared-20261119-154928-cc4e33`, cùng quyết định v2 "Thu hẹp" (bỏ kho DN) dựa trên `R-S4-after-20261119-170556-5b35f2`. Tôi uỷ quyền cho trưởng nhóm Vũ Văn Trường ký thay ô "PIC ký" ở B8 và C12. Exit ticket không dùng AI.

### Bằng chứng

- Commit: `7a3a5d1` (tiêu chí đã ký, `signed_by` Lê Huy Anh), `4aeda6d` (B8 cột v1).
- Phiếu A mục A1, A3, A4, A5; Phiếu B mục B1, B3, B7.4, B8; Phiếu C mục C7 (phạm vi), C12 (quyết định v2).

### Exit ticket

- Một điều học được: ngưỡng phải được viết và ký trước khi xem kết quả; nếu ký sau khi đã đo, nhóm dễ nới ngưỡng để vừa số.
- Một điều còn chưa chắc: `escalation_rate_max` 0,25 và `cost_per_ticket_vnd_max` 6.000đ có còn hợp lý khi pilot mở 100% ở cả hai depot và giá LLM/thời gian duyệt thay đổi hay không.

## TranThiNhai-2A202603911

### Phần việc phụ trách

Vận hành và pháp lý. Câu 1.2, 2.4, 2.5, 2.10, giờ cao điểm, runbook. Phiếu A mục A1 (mục tiêu chị Oanh / chị Hạnh), A2 (telemetry);
Phiếu B mục B4, B5, B6, B7.5, B7.6; Phiếu C mục C1 (pre-mortem), C4 (HAZOP của thẻ), C10, C11 (runbook phần 4–5). Thẻ S4 không cần điền C3. File `config/operating_gates.json` mục `operations` và
`legal`, `submission/submission.json`.

### Đóng góp cụ thể

- Duyệt cổng vận hành và pháp lý (`config/operating_gates.json` mục `operations` và `legal`): PIC NV-TUNG, người duyệt NV-HANH, 1 người trực × 6 ca/giờ, chờ tối đa 45 phút, 5 điều kiện dừng, kênh báo tin Zalo + gọi điện, chặn `recipient_contact` và `customer_note`, ghi lỗi hãng phải có nguyên nhân.
- Duyệt, chỉnh và chịu trách nhiệm HAZOP vòng 1 trên `issue_refund` (≥ 3 dòng kỹ thuật + 4 dòng ngoài kỹ thuật), checklist 9 nhóm việc có PIC, pre-mortem 4 lăng kính, runbook phần 1–3 và mục Giờ cao điểm khớp config.
- Duyệt Phiếu A A1 (mục tiêu của chị Oanh và chị Hạnh), A2 (telemetry ngưỡng vàng/đỏ); soát `submission/submission.json` (`team`, `members`, `decision_v1`).
- Soát runbook với config và report (`R-base-prepared-20261119-154928-cc4e33`: 6 ca/ngày vào hàng chờ, chờ lâu nhất 0 phút, 0 ca ùn); chịu trách nhiệm giải thích PIC, người duyệt, số người trực và điều kiện dừng lúc demo.

**Dùng AI:** Bản nháp các phần của vai tôi được Claude (Claude Code) soạn trong phiên làm việc của trưởng nhóm Vũ Văn Trường:
- Phiếu A: A1 (mục tiêu của chị Oanh và chị Hạnh), A2 (telemetry, ngưỡng vàng và đỏ).
- Phiếu B: B4 (HAZOP trên `issue_refund` và 4 dòng ngoài kỹ thuật), B5 (checklist 9 nhóm), B6 (pre-mortem 4 lăng kính), B7.5 (runbook 1–3), B7.6 (giờ cao điểm, gồm ba dòng [Vòng 2 · S4]).
- Phiếu C: C1, C4, C10, C11 (runbook 4–5); `stop_conditions` vòng 2 (ngưỡng `peak_hour_review_load`, ngân sách hoàn theo ngày).
- `config/operating_gates.json` mục `operations` và `legal`; `submission/submission.json` (team, members, decision_v1).

Tôi đã đọc lại runbook và đối chiếu với config, gồm: PIC NV-TUNG, người duyệt NV-HANH, 1 người × 6 ca/giờ, chờ tối đa 45 phút, 5 điều kiện dừng, hai trường dữ liệu cá nhân bị chặn. Exit ticket không dùng AI.

### Bằng chứng

- Commit: `4aeda6d` (cổng `operations`/`legal`, Phiếu B mục B4–B7.6).
- Phiếu A mục A1 (1.2), A2; Phiếu B mục B4, B5, B6, B7.5, B7.6; Phiếu C mục C1, C4, C10, C11.

### Exit ticket

- Một điều học được: runbook và PIC rõ ràng biến cổng từ "điều kiện trong code" thành "việc ai bấm trong 15 phút", nên vận hành không phụ thuộc vào một người nhớ hết.
- Một điều còn chưa chắc: với cao điểm 14 ca chuyển người trong một giờ, một người duyệt × 6 ca/giờ có đủ không, và lòng tin của nhân viên vào trợ lý sẽ thay đổi thế nào sau khi họ thấy một ca sai.
