Phiên bản Python 3.11.5
Cài đặt các thư viện cần thiết bằng câu lệnh `pip install -r requirements.txt`. 



# DATA 
Có 3 folder con trong folder data, tương ứng với đó là các bộ dữ liệu:
 - Folder "OR-Library":
 - File "Realworld dataset" được đi kèm bài báo hướng dẫn. Được lọc sẵn và dùng để thử nghiệm theo thang điểm của bài báo.
 - File "API binance" là dữ liệu được gọi từ API của sàn giao dịch Binance. Có các sheet giá lấy được không cùng ngày với nhau. Ví dụ:SHIB_USD - giá từ 2021-10-5, khác với phần còn lại. Hay như LUNC dữ liệu không liên tục. Các sheet cần xem xét vì không theo chuẩn là: FTT, SHIB, LUNC, NEAR. Trong folder còn có các file vector tỉ lệ lợi nhuận chia theo các thang đo như theo ngày, tuần, tháng và chia theo mốc thời gian (Trước và sau cuộc khủng hoảng LUNA 2022-05-06).

`percentReturns{Time distance}Data.xlsx`: gồm nhiều vector phần trăm lợi nhuận của nhiều đồng tiền mã hóa nhất có thể, từ ngày 14/10/2020 - 11/30/2022 (không bao gồm, LUNA, FTT, SHIBA)

`percentReturns{Time distance}DataBeforeLunc.xlsx`: gồm nhiều vector phần trăm lợi nhuận của các đồng tiền mã hóa trước ngày xảy ra khủng hoảng LUNA, từ ngày 10/14/2020 - 6/05/2022 (lúc giá chưa giảm)

`percentReturns{Time distance}DataAfterLunc.xlsx`: gồm nhiều vector phần trăm lợi nhuận của các đồng tiền mã hóa bao gồm cả những ngày xảy ra khủng hoảng LUNA, từ ngày 10/14/2020 - 26/05/2022 (Vì sau đó giá theo API không còn liên tục.)

# File 
`data_processing.ipynb`: Dùng để xử lý dữ liệu từ file `API.xlsx`. Path ở đầu file là nơi đọc file api. Còn ở cuối file là nơi để lưu file.

`portfolio_ga.ipynb`: file chạy mô hình.


