#import "edition.typ": edition, stack-lines
#import "theme.typ": apply-theme
#import "components.typ": cover

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
#include "chapters/01-bay-ngay.typ"
#include "chapters/02-dich-den-va-nen-tang.typ"
#include "chapters/03-tu-niem-xu-trong-kinh.typ"
#include "chapters/04-duyen-khoi.typ"
#include "chapters/05-phuong-phap-mahasi.typ"
#include "chapters/06-trien-cai-giac-chi.typ"
#include "chapters/07-doi-song-tai-gia.typ"
#include "chapters/08-lo-trinh-thay-khoa-thien.typ"
#include "chapters/09-an-toan.typ"
#include "chapters/10-nhap-luu.typ"
#include "chapters/11-ha-phan-va-sa-mon-qua.typ"
#include "chapters/12-ban-do-tue.typ"
#include "chapters/13-tu-dieu-de-van-hanh.typ"
#include "appendices/a-nhat-ky.typ"
#include "appendices/b-nhan-tham-chieu.typ"
#include "appendices/c-faq.typ"
#include "appendices/d-thuat-ngu.typ"
#include "appendices/e-ban-do-quyet-dinh.typ"
#include "chapters/99-nguon.typ"
