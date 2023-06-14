using System;

namespace BogusTestApp.Models
{
    public class Order  // 주문 테이블
    {
        public Guid Id { get; set; }    // 키 값
        public DateTime Date { get; set; }  // 주문 일자
        public decimal OrderValue { get; set; } // 주문갯수
        public bool Shipped { get; set; }   // 선적 여부

    }
}
