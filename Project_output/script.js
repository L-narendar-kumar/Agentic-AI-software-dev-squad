// script.js

// Calculator state object
const calculator = {
    displayValue: '0',
    firstOperand: null,
    waitingForSecondOperand: false,
    operator: null,
};

/**
 * Updates the calculator display with the current displayValue.
 * Assumes an HTML input element with class 'calculator-screen'.
 */
function updateDisplay() {
    const display = document.querySelector('.calculator-screen');
    if (display) {
        display.value = calculator.displayValue;
    }
}

/**
 * Handles digit input.
 * If waiting for a second operand, starts a new number.
 * Otherwise, appends the digit to the current displayValue.
 * @param {string} digit The digit character ('0'-'9').
 */
function inputDigit(digit) {
    const { displayValue, waitingForSecondOperand } = calculator;

    if (waitingForSecondOperand === true) {
        calculator.displayValue = digit;
        calculator.waitingForSecondOperand = false;
    } else {
        // If displayValue is '0', replace it with the digit; otherwise, append.
        calculator.displayValue = displayValue === '0' ? digit : displayValue + digit;
    }
}

/**
 * Handles decimal point input.
 * Prevents multiple decimal points in a single number.
 * If waiting for a second operand, starts a new number with '0.'.
 * @param {string} dot The decimal point character ('.').
 */
function inputDecimal(dot) {
    // If waitingForSecondOperand is true, start a new number '0.'
    if (calculator.waitingForSecondOperand === true) {
        calculator.displayValue = '0.';
        calculator.waitingForSecondOperand = false;
        return;
    }

    // If the current displayValue does not already contain a decimal point
    if (!calculator.displayValue.includes(dot)) {
        calculator.displayValue += dot;
    }
}

/**
 * Performs the arithmetic calculation based on the operands and operator.
 * Handles division by zero.
 * @param {string|number} firstOperand The first number in the operation.
 * @param {string|number} secondOperand The second number in the operation.
 * @param {string} operator The arithmetic operator ('+', '-', '*', '/').
 * @returns {number|string} The result of the calculation, or 'Error' for division by zero.
 */
function performCalculation(firstOperand, secondOperand, operator) {
    const num1 = parseFloat(firstOperand);
    const num2 = parseFloat(secondOperand);

    // If either operand is not a valid number, return the second operand
    // or handle as an error, depending on desired behavior.
    // For a calculator, returning the second operand might be acceptable
    // if the first was just an empty string or similar.
    if (isNaN(num1) || isNaN(num2)) {
        return num2;
    }

    switch (operator) {
        case '+':
            return num1 + num2;
        case '-':
            return num1 - num2;
        case '*':
            return num1 * num2;
        case '/':
            if (num2 === 0) {
                // Handle division by zero edge case
                alert("Error: Division by zero is not allowed.");
                return 'Error';
            }
            return num1 / num2;
        default:
            // Should not be reached if operator is always one of the above
            return num2;
    }
}

/**
 * Handles operator input ('+', '-', '*', '/').
 * Manages operator chaining and pending calculations.
 * @param {string} nextOperator The operator character clicked.
 */
function handleOperator(nextOperator) {
    const { firstOperand, displayValue, operator } = calculator;
    const inputValue = parseFloat(displayValue);

    // If an operator already exists and waitingForSecondOperand is true,
    // it means the user is changing the operator before entering the second number.
    // In this case, just update the operator and return.
    if (operator && calculator.waitingForSecondOperand) {
        calculator.operator = nextOperator;
        return;
    }

    // If firstOperand is null, set the current displayValue as the firstOperand
    if (firstOperand === null) {
        calculator.firstOperand = inputValue;
    } else if (operator) {
        // If an operator exists, perform the pending calculation
        const result = performCalculation(firstOperand, displayValue, operator);

        if (result === 'Error') {
            // If division by zero occurred, reset calculator and display error
            calculator.displayValue = 'Error';
            resetCalculator(); // Reset all state except displayValue
            updateDisplay();
            return;
        }

        calculator.displayValue = String(result);
        calculator.firstOperand = result; // The result becomes the new firstOperand for chaining
    }

    calculator.waitingForSecondOperand = true; // Next digit input should start a new number
    calculator.operator = nextOperator; // Store the new operator
}

/**
 * Resets the calculator to its initial state.
 */
function resetCalculator() {
    calculator.displayValue = '0';
    calculator.firstOperand = null;
    calculator.waitingForSecondOperand = false;
    calculator.operator = null;
}

// Event listener for button clicks on the calculator keys container.
// Assumes an HTML div with class 'calculator-keys' containing buttons.
const keys = document.querySelector('.calculator-keys');
if (keys) {
    keys.addEventListener('click', (event) => {
        const { target } = event; // Get the clicked element

        // Check if the clicked element is a button. If not, do nothing.
        if (!target.matches('button')) {
            return;
        }

        // Handle operator buttons (+, -, *, /)
        if (target.classList.contains('operator') && target.value !== '=') {
            handleOperator(target.value);
            updateDisplay();
            return;
        }

        // Handle decimal button
        if (target.classList.contains('decimal')) {
            inputDecimal(target.value);
            updateDisplay();
            return;
        }

        // Handle 'All Clear' button
        if (target.classList.contains('all-clear')) {
            resetCalculator();
            updateDisplay();
            return;
        }

        // Handle 'Equals' button
        if (target.classList.contains('equal-sign')) {
            // If there's no first operand or operator, do nothing
            if (calculator.firstOperand === null || calculator.operator === null) {
                return;
            }

            const result = performCalculation(calculator.firstOperand, calculator.displayValue, calculator.operator);

            if (result === 'Error') {
                // If division by zero occurred, reset calculator and display error
                calculator.displayValue = 'Error';
                resetCalculator(); // Reset all state except displayValue
                updateDisplay();
                return;
            }

            calculator.displayValue = String(result);
            calculator.firstOperand = null; // Clear first operand after equals
            calculator.operator = null; // Clear operator after equals
            calculator.waitingForSecondOperand = true; // Next digit should start a new number
            updateDisplay();
            return;
        }

        // If it's a digit button
        inputDigit(target.value);
        updateDisplay();
    });
}

// Initial display update when the script loads
updateDisplay();
