#import "theme.typ": apply-theme
#import "components.typ": cover

#let publication-author = [CS Chánh Niệm + ChatGPT]

#set document(
  title: "Hướng Đến Nhập Lưu",
  author: ("CS Chánh Niệm + ChatGPT",),
  description: "Sổ tay Niệm xứ cho người tại gia theo truyền thống Mahāsi, đối chiếu Kinh tạng Pāli và Thanh Tịnh Đạo",
  keywords: ("Niệm xứ", "Mahāsi", "Nhập lưu", "Thiền Vipassanā", "Thanh Tịnh Đạo"),
)

#show: apply-theme

#cover(
  [Hướng Đến #linebreak() Nhập Lưu],
  [Sổ tay Niệm xứ cho người tại gia theo truyền thống Mahāsi, đối chiếu Kinh tạng Pāli và Thanh Tịnh Đạo],
  author: publication-author,
)

#include "chapters/00-frontmatter.typ"
#include "chapters/01-bay-ngay.typ"
#include "chapters/02-dich-den-va-nen-tang.typ"
#include "chapters/03-tu-niem-xu-trong-kinh.typ"
#include "chapters/04-phuong-phap-mahasi.typ"
#include "chapters/05-trien-cai-giac-chi.typ"
#include "chapters/06-doi-song-tai-gia.typ"
#include "chapters/07-lo-trinh-thay-khoa-thien.typ"
#include "chapters/08-an-toan.typ"
#include "chapters/09-ban-do-tue.typ"
#include "chapters/10-nhap-luu.typ"
#include "appendices/a-nhat-ky.typ"
#include "appendices/b-nhan-tham-chieu.typ"
#include "appendices/c-faq.typ"
#include "appendices/d-thuat-ngu.typ"
#include "chapters/99-nguon.typ"
