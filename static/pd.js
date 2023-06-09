 document.getElementById("customer-form").addEventListener("submit", function (event) {
   event.preventDefault(); // Prevent form submission

   // Get the customer ID from the input field
   var customerId = document.getElementById("customer-id").value;

   // Create a new XMLHttpRequest object
   var xhr = new XMLHttpRequest();

   // Configure the request
   xhr.open("GET", "recommendations?customerId=" + encodeURIComponent(customerId), true);

   // Define the callback function when the request is complete
   xhr.onload = function () {
     if (xhr.status === 200) {
       // Request succeeded, parse the response
       var response = JSON.parse(xhr.responseText);

       // Display the recommended products
       var resultDiv = document.getElementById("result");
       resultDiv.innerHTML = "<h3>Recommended Products:</h3>";
       var productList = response.products;
       for (var i = 0; i <productList.length; i++) {
         var productName = productList[i];
         // resultDiv.innerHTML += "<p>" + productName + "</p>";
         resultDiv.innerHTML += "<div class='product-box'><p class='product-name'>" + productName + "</p></div>";
       }

     } else {
       // Request failed, display an error message
       var resultDiv = document.getElementById("result");
       resultDiv.innerHTML = "<p>Error retrieving recommendations. Please check customerId.</p>";
     }
   };

   // Send the request
   xhr.send();
 });
