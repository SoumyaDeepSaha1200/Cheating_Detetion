const currencyList = [
    "USD", "EUR", "GBP", "INR", "AUD", "CAD", "SGD", "JPY",
    "UZS", "PKR", "BDT", "LKR", "THB", "VND", "RUB"
];

const fromCurrency = document.getElementById('fromCurrency');
const toCurrency = document.getElementById('toCurrency');

currencyList.forEach(currency => {
    const option1 = document.createElement('option');
    option1.value = currency;
    option1.textContent = currency;
    fromCurrency.appendChild(option1);

    const option2 = document.createElement('option');
    option2.value = currency;
    option2.textContent = currency;
    toCurrency.appendChild(option2);
});

async function convertCurrency() {
    const amount = document.getElementById('amount').value;
    const from = fromCurrency.value;
    const to = toCurrency.value;

    if (!amount || !from || !to) {
        alert("Please fill in all fields");
        return;
    }

    const response = await fetch(`https://api.exchangerate-api.com/v4/latest/${from}`);
    const data = await response.json();

    const rate = data.rates[to];
    const result = (amount * rate).toFixed(2);

    document.getElementById('result').textContent = `${amount} ${from} = ${result} ${to}`;
}
