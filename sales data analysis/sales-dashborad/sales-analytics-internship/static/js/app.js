document.addEventListener('DOMContentLoaded', function() {
    // Load data from Flask endpoint
    fetch('/get_analytics')
        .then(response => response.json())
        .then(data => {
            // Update KPIs
            document.getElementById('totalRevenue').textContent = 
                `$${data.metrics.total_revenue.toLocaleString('en-US', {maximumFractionDigits: 0})}`;
            document.getElementById('avgOrderValue').textContent = 
                `$${data.metrics.avg_order_value.toLocaleString('en-US', {maximumFractionDigits: 2})}`;
            document.getElementById('conversionRate').textContent = 
                `${(data.metrics.conversion_rate * 100).toFixed(1)}%`;
            
            // Update recommendations
            const recList = document.getElementById('recommendationsList');
            data.recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                recList.appendChild(li);
            });
            
            // Update timestamps
            document.getElementById('generationDate').textContent = 
                new Date(data.generated_at).toLocaleString();
            document.getElementById('updateTime').textContent = 
                `Last updated: ${new Date().toLocaleTimeString()}`;
        });
    
    // Add interactive elements
    document.querySelectorAll('.chart-image').forEach(img => {
        img.addEventListener('click', function() {
            this.classList.toggle('zoom');
        });
    });
});