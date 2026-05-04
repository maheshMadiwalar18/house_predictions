document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const predictBtn = document.getElementById('predict-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    const resultDisplay = document.getElementById('result-display');
    const priceOutput = document.getElementById('price-output');
    const errorBox = document.getElementById('error-box');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Get and Validate values
        const areaRaw = document.getElementById('area').value;
        const bedroomsRaw = document.getElementById('bedrooms').value;
        const bathroomsRaw = document.getElementById('bathrooms').value;
        const ageRaw = document.getElementById('age').value;

        // Prevent empty inputs
        if (!areaRaw || !bedroomsRaw || !bathroomsRaw || !ageRaw) {
            showError('All fields are required.');
            return;
        }

        // Convert to Numbers explicitly
        const payload = {
            area: Number(areaRaw),
            bedrooms: Number(bedroomsRaw),
            bathrooms: Number(bathroomsRaw),
            age: Number(ageRaw)
        };

        // Prevent negative values
        if (payload.area <= 0 || payload.bedrooms < 0 || payload.bathrooms < 0 || payload.age < 0) {
            showError('Please enter valid positive numbers.');
            return;
        }

        // 2. Debugging: Show payload in console
        console.log('Sending Payload to API:', payload);

        // 3. Prepare UI for loading
        setLoading(true);
        hideError();
        resultDisplay.classList.remove('active');

        // 4. API Call
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Server error');
            }

            const data = await response.json();
            
            // Debugging: Show response in console
            console.log('API Response:', data);

            if (data.error) {
                throw new Error(data.error);
            }

            // Map specifically to data.price as per requirement
            const predictedPrice = data.price || 0;
            
            displayResult(predictedPrice);

        } catch (error) {
            console.error('Fetch error:', error);
            showError('Server error. Please try again.');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            predictBtn.disabled = true;
            btnText.style.opacity = '0';
            btnSpinner.style.display = 'block';
        } else {
            predictBtn.disabled = false;
            btnText.style.opacity = '1';
            btnSpinner.style.display = 'none';
        }
    }

    function displayResult(price) {
        // Format as currency: ₹XX,XXX (no extra scaling)
        const formattedPrice = new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(price);

        priceOutput.textContent = formattedPrice;
        resultDisplay.classList.add('active');
    }

    function showError(message) {
        errorBox.textContent = message;
        errorBox.style.display = 'block';
    }

    function hideError() {
        errorBox.style.display = 'none';
    }
});
