#import "edition.typ": edition, stack-lines
#import "theme.typ": apply-theme
#import "components.typ": cover, part

#set document(
  title: edition.metadata.title,
  author: (edition.metadata.author,),
  description: edition.metadata.description,
  keywords: edition.metadata.keywords,
)

#show: apply-theme

#cover(
  stack-lines(edition.cover.title_lines),
  edition.metadata.description,
  author: edition.metadata.author,
)

#include "chapters/00-frontmatter.typ"
#part([Phần I — Bắt đầu thực hành], [Từ buổi ngồi đầu tiên đến nền giáo lý gần nhất: bảy ngày đầu, đích đến của con đường, bốn lĩnh vực quán sát và cơ chế thọ–ái.])

#include "chapters/01-bay-ngay.typ"
#include "chapters/02-dich-den-va-nen-tang.typ"
#include "chapters/03-tu-niem-xu-trong-kinh.typ"
#include "chapters/04-duyen-khoi.typ"
#part([Phần II — Phương pháp và đời sống], [Cách ngồi, cách ghi nhận, cách làm việc với triền cái, cách đem niệm vào một ngày thường và các ngưỡng an toàn cần nhớ.])

#include "chapters/05-phuong-phap-mahasi.typ"
#include "chapters/06-trien-cai-giac-chi.typ"
#include "chapters/07-doi-song-tai-gia.typ"
#include "chapters/08-lo-trinh-thay-khoa-thien.typ"
#include "chapters/09-an-toan.typ"
#part([Phần III — Hướng về Nhập lưu], [Ba kiết sử đầu, vị trí của chúng trong năm hạ phần và bốn quả, rồi khung Tứ Thánh Đế gắn với một phản ứng thật trong đời sống.])

#include "chapters/10-nhap-luu.typ"
#include "chapters/11-ha-phan-va-sa-mon-qua.typ"
#include "chapters/13-tu-dieu-de-van-hanh.typ"
#part([Phần IV — Đọc sâu khi đã có người hướng dẫn], [Bản đồ tuệ là tài liệu tra cứu cho người đã hành đều, biết ngưỡng an toàn và có người kiểm tra cùng. Người mới không cần đọc phần này trong những tháng đầu.])

#include "chapters/12-ban-do-tue.typ"
#include "appendices/a-nhat-ky.typ"
#include "appendices/b-nhan-tham-chieu.typ"
#include "appendices/c-faq.typ"
#include "appendices/d-thuat-ngu.typ"
#include "appendices/e-ban-do-quyet-dinh.typ"
#include "chapters/99-nguon.typ"
