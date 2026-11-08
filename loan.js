// loan.js - เงินกู้ลดต้นลดดอก ใช้ผลเฉลยทั่วไปของความสัมพันธ์เวียนเกิด
// a_n = (1+i)a_{n-1} - x  ->  a_n = (1+i)^n * a0 - x * ((1+i)^n - 1) / i
const readline = require("readline/promises");

// ผลเฉลยทั่วไป: ยอดหนี้คงเหลือหลังผ่อน n งวด
//ประกาศฟังก์ชันรับพารามิเตอร์ 4 ตัว: เงินต้น a0, ดอกเบี้ยต่อเดือน i, ค่างวด x, จำนวนงวดที่ผ่านไป n
function balance(a0, i, x, n) {
  if (i === 0) return a0 - n * x;               // กรณี i = 0
  const g = Math.pow(1 + i, n);                // คำนวณ (1+i)ⁿ เก็บไว้ในตัวแปร g เพราะใช้สองรอบ จะได้ไม่ต้องคำนวณซ้ำ
  return g * a0 - (x * (g - 1)) / i;          // คืนค่าตามสูตร aₙ = (1+i)ⁿ·a₀ − x·((1+i)ⁿ − 1)/i
}

// หาค่างวด x โดยให้ a_N = 0
function payment(a0, i, N) {
  if (i === 0) return a0 / N;
  const g = Math.pow(1 + i, N);
  return (a0 * i * g) / (g - 1);
}
//รับข้อมูลจากผู้ใช้งาน
async function calculateLoan() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log("\n--- Loan Payment Calculator ---");
  const a0 = parseFloat(await rl.question("Enter the loan amount (a0): "));
  const r = parseFloat(await rl.question("Enter the annual interest rate (percent): "));
  const N = parseInt(await rl.question("Enter the number of months to repay: "), 10);
  rl.close();
//ตรวจสอบความถูกต้อง ถ้าอย่างใดอย่างหนึ่งเป็นจริงให้แจ้งเตือนแล้วจบโปรแกรม
//มีค่าใดไม่ใช่ตัวเลข (NaN)
//จำนวนเดือนน้อยกว่า 1
//เงินกู้ ≤ 0
// อันตราดอกเบี้ยต้องไม่ติดลบ
  if ([a0, r, N].some(Number.isNaN) || N < 1 || a0 <= 0 || r < 0) {
    console.log("Invalid input. Please enter valid numbers (months must be at least 1).");
    return;
  }

  const i = r / 100 / 12; // ดอกเบี้ยต่อเดือน (เป็นทศนิยม)
  const x = payment(a0, i, N);

  console.log(`\nYour monthly payment is: ${x.toFixed(2)}`);
  console.log("\nMonth | Remaining balance");
  for (let n = 1; n <= N; n++) {
    const b = n === N ? 0 : balance(a0, i, x, n); // งวดสุดท้ายปรับเศษทศนิยมให้เป็น 0
    console.log(`${String(n).padStart(5)} | ${b.toFixed(2)}`);
  }

  const totalPaid = x * N;
  console.log(`\nTotal payment after ${N} months: ${totalPaid.toFixed(2)}`);
  console.log(`Total interest paid: ${(totalPaid - a0).toFixed(2)}`);
}

calculateLoan();
