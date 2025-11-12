// Simple Calculator Prototype
// A basic calculator implementation

class Calculator {
  constructor() {
    this.result = 0;
  }

  add(num) {
    this.result += num;
    return this;
  }

  subtract(num) {
    this.result -= num;
    return this;
  }

  multiply(num) {
    this.result *= num;
    return this;
  }

  divide(num) {
    if (num === 0) {
      throw new Error('Division by zero');
    }
    this.result /= num;
    return this;
  }

  getResult() {
    return this.result;
  }

  reset() {
    this.result = 0;
    return this;
  }
}

// Example usage
const calc = new Calculator();
const result = calc
  .add(10)
  .multiply(2)
  .subtract(5)
  .getResult();

console.log('Result:', result); // Output: 15

