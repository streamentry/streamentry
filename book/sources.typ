// Tên đọc được của các nguồn. Mã K, P, V, R chỉ còn hiện ở Bản đồ nguồn
// (Chương 99); trong thân sách, người đọc và người nghe gặp tên bài kinh,
// tên bộ và số bài viết đầy đủ, kèm liên kết về đúng mục của bản đồ nguồn.

#let _an-chuong = (
  "3": "Ba Pháp",
  "4": "Bốn Pháp",
  "5": "Năm Pháp",
  "6": "Sáu Pháp",
  "7": "Bảy Pháp",
  "10": "Mười Pháp",
)

// Vị trí theo cách viết đầy đủ, không viết tắt tên bộ.
#let _vi-tri(bo, so) = {
  if bo == "DN" { "Trường Bộ, bài số " + so }
  else if bo == "MN" { "Trung Bộ, bài số " + so }
  else if bo == "SN" {
    let (chuong, bai) = so.split(".")
    "Tương Ưng Bộ, chương " + chuong + ", bài số " + bai
  } else if bo == "AN" {
    let (chuong, bai) = so.split(".")
    "Tăng Chi Bộ, chương " + _an-chuong.at(chuong) + ", bài số " + bai
  } else if bo == "Ud" {
    let (chuong, bai) = so.split(".")
    "Tiểu Bộ, Kinh Phật Tự Thuyết, chương " + chuong + ", bài số " + bai
  } else if bo == "Iti" { "Tiểu Bộ, Kinh Phật Thuyết Như Vậy, bài số " + so }
  else if bo == "Dhp" { "Tiểu Bộ, Kinh Pháp Cú, câu kệ số " + so }
  else { panic("bộ kinh chưa khai báo: " + bo) }
}

// Mỗi mục: (tên, bộ, số). Tên có sẵn trong truyền thống Việt được viết hoa;
// bài chưa có tên Việt quen thuộc được gọi bằng nội dung ("bài kinh về ...").
#let _kinh = (
  K01: ("Kinh Niệm Xứ", "MN", "10"),
  K02: ("bài kinh về bốn yếu tố đưa đến Nhập lưu", "SN", "55.50"),
  K03: ("bài kinh về bốn phẩm chất của bậc Nhập lưu", "SN", "55.4"),
  K04: ("bài kinh về mục đích của giới", "AN", "10.1"),
  K05: ("Kinh Chuyển Pháp Luân", "SN", "56.11"),
  K06: ("bài kinh về người nhập dòng", "SN", "55.5"),
  K07: ("Kinh Trạm Xe", "MN", "24"),
  K08: ("Kinh Đại Bát Niết-bàn", "DN", "16"),
  K09: ("Kinh Năm Sợ Hãi Thù Hận", "SN", "12.41"),
  K10: ("bài kinh về các bậc hữu học", "AN", "3.88"),
  K11: ("Kinh Tất Cả Lậu Hoặc", "MN", "2"),
  K12: ("Kinh Nhập Tức Xuất Tức Niệm", "MN", "118"),
  K13: ("bài kinh về cách quân bình các giác chi", "SN", "46.53"),
  K14: ("bài kinh về niệm chết", "AN", "6.19"),
  K15: ("Kinh Giáo Thọ Thi-ca-la-việt", "DN", "31"),
  K16: ("bài kinh về chỉ quán song hành", "AN", "4.170"),
  K17: ("Kinh Khemaka", "SN", "22.89"),
  K18: ("bài kinh dạy dân làng Veḷudvāra", "SN", "55.7"),
  K19: ("Kinh Thể Nhập", "AN", "6.63"),
  K20: ("Tiểu Kinh Phương Quảng", "MN", "44"),
  K21: ("bài kinh về sự lắng dịu năm sợ hãi", "AN", "10.92"),
  K22: ("Kinh Thức Ăn", "SN", "46.51"),
  K23: ("Đại Kinh Bốn Mươi", "MN", "117"),
  K24: ("bài kinh về mười kiết sử", "AN", "10.13"),
  K25: ("Kinh Phân Tích Bát Chánh Đạo", "SN", "45.8"),
  K26: ("Kinh Phân Tích Duyên Khởi", "SN", "12.2"),
  K27: ("Kinh Thế Gian", "SN", "12.44"),
  K28: ("Kinh Mũi Tên", "SN", "36.6"),
  K29: ("Đại Kinh Đoạn Tận Ái", "MN", "38"),
  K30: ("Kinh Sáu Sáu", "MN", "148"),
  K31: ("Kinh Chánh Tri Kiến", "MN", "9"),
  K32: ("bài kinh về bốn quả Sa-môn", "SN", "45.35"),
  K33: ("Kinh Bố-tát", "Ud", "5.5"),
  K34: ("Kinh Sa-môn Quả", "DN", "2"),
  K35: ("Kinh Vô Ngã Tướng", "SN", "22.59"),
  K36: ("Đại Kinh Māluṅkyaputta", "MN", "64"),
  K37: ("Kinh Kiết Sử", "SN", "41.1"),
  K38: ("Kinh Hạnh Con Chó", "MN", "57"),
  K39: ("bài kinh về các hạng người thực hành để chứng quả", "SN", "48.18"),
  K40: ("bài kinh về đích đến của đời sống Sa-môn", "SN", "45.36"),
  K41: ("câu kệ về quả Dự lưu", "Dhp", "178"),
  K42: ("bài kinh về năm nghề buôn bán cư sĩ nên tránh", "AN", "5.177"),
  K43: ("bài kinh hỏi về Niết-bàn", "SN", "38.1"),
  K44: ("bài kinh về hai lối mắc kẹt quanh sự hiện hữu", "Iti", "49"),
  K45: ("Kinh Đêm Trăng Rằm", "SN", "22.82"),
  K46: ("Kinh Tâm Hoang Vu", "MN", "16"),
  K47: ("Kinh Tư Sát", "MN", "47"),
  K48: ("Kinh Caṅkī", "MN", "95"),
  K49: ("bài kinh về kết quả của giới hạnh", "AN", "3.78"),
  K50: ("Kinh Samaṇamuṇḍika", "MN", "78"),
  K51: ("bài kinh về cách bậc A-la-hán dùng chữ “tôi”", "SN", "1.25"),
  K52: ("bài kinh về bốn phương diện của năm uẩn", "SN", "22.56"),
  K53: ("Kinh Uẩn", "SN", "22.48"),
  K54: ("bài kinh về cách đối trị cơn buồn ngủ", "AN", "7.61"),
)

// Nguồn ngoài kinh điển: (tên đầy đủ, tên ngắn để nhắc lại).
#let _khac = (
  P01: ("Practical Insight Meditation (Thiền Minh Sát Thực Hành)", "Thiền Minh Sát Thực Hành"),
  P02: ("The Progress of Insight (Tiến Trình Minh Sát)", "Tiến Trình Minh Sát"),
  V01: ("Thanh Tịnh Đạo (Visuddhimagga)", "Thanh Tịnh Đạo"),
  R01: ("nghiên cứu của Lindahl và cộng sự năm 2017 về những trải nghiệm thiền khó khăn", "nghiên cứu của Lindahl"),
  R02: ("tổng quan hệ thống của Farias và cộng sự năm 2020 về biến cố bất lợi khi hành thiền", "tổng quan của Farias"),
  R03: ("hướng dẫn ứng phó căng thẳng của Tổ chức Y tế Thế giới", "hướng dẫn của Tổ chức Y tế Thế giới"),
  R04: ("tài liệu của Tổ chức Y tế Thế giới về người có thể đang nghĩ đến tự tử", "tài liệu phòng ngừa tự tử của Tổ chức Y tế Thế giới"),
  R05: ("tài liệu về loạn thần của Viện Sức khỏe Tâm thần Quốc gia Hoa Kỳ", "tài liệu về loạn thần của Viện Sức khỏe Tâm thần Hoa Kỳ"),
  R06: ("hướng dẫn điều trị loạn thần của Dịch vụ Y tế Quốc gia Anh", "hướng dẫn của Dịch vụ Y tế Quốc gia Anh"),
  R07: ("hướng dẫn nhận biết đột quỵ của Trung tâm Kiểm soát và Phòng ngừa Dịch bệnh Hoa Kỳ", "hướng dẫn nhận biết đột quỵ"),
  R08: ("hướng dẫn về dấu hiệu nhồi máu cơ tim của Trung tâm Kiểm soát và Phòng ngừa Dịch bệnh Hoa Kỳ", "hướng dẫn về nhồi máu cơ tim"),
  R09: ("hướng dẫn sơ cứu co giật của Trung tâm Kiểm soát và Phòng ngừa Dịch bệnh Hoa Kỳ", "hướng dẫn sơ cứu co giật"),
  R10: ("Nghị định 200/2025/NĐ-CP về Tổng đài khẩn cấp quốc gia 112", "Nghị định về Tổng đài 112"),
  R11: ("văn bản quy hoạch kho số viễn thông quy định các đầu số 113, 114 và 115", "quy hoạch kho số 113, 114, 115"),
)

#let _dich(code) = label("nguon-" + lower(code))

// Tên ngắn, không kèm vị trí: "Kinh Niệm Xứ".
#let ten(code) = {
  let entry = if code in _kinh { _kinh.at(code).first() } else { _khac.at(code).at(1) }
  link(_dich(code), entry)
}

// Tên kèm vị trí đầy đủ: "Kinh Niệm Xứ (Trung Bộ, bài số 10, phần quán thân)".
#let nguon(code, doan: none) = {
  if code in _kinh {
    let (name, bo, so) = _kinh.at(code)
    link(_dich(code))[#name (#_vi-tri(bo, so)#if doan != none [, #doan])]
  } else {
    link(_dich(code))[#_khac.at(code).first()#if doan != none [, #doan]]
  }
}

// Tiêu đề một mục trong Bản đồ nguồn: "Kinh Niệm Xứ (Trung Bộ, bài số 10)".
#let tieu-de(code) = {
  let (name, bo, so) = _kinh.at(code)
  let first = name.first()
  upper(first) + name.slice(first.len()) + " (" + _vi-tri(bo, so) + ")"
}

// Cách viết tắt quốc tế, chỉ dùng trong Bản đồ nguồn: "MN 10".
#let viet-tat(code) = {
  let (_, bo, so) = _kinh.at(code)
  bo + " " + so
}

// Một danh sách nguồn đọc liền mạch: "Kinh Niệm Xứ, Kinh Mũi Tên và sách
// Tiến Trình Minh Sát". Phần tử không phải mã (ví dụ [Phụ lục B]) giữ nguyên.
#let danh-sach(items) = {
  let parts = items.map(item => {
    if type(item) == str and item.starts-with("P") { [sách _#ten(item)_] }
    else if type(item) == str { ten(item) }
    else { item }
  })
  if parts.len() == 1 { parts.first() }
  else { parts.slice(0, -1).join(", ") + [ và ] + parts.last() }
}

// Như `ten`, nhưng viết hoa chữ đầu khi tên đứng đầu câu.
#let Ten(code) = {
  let entry = if code in _kinh { _kinh.at(code).first() } else { _khac.at(code).at(1) }
  let first = entry.first()
  link(_dich(code), upper(first) + entry.slice(first.len()))
}
