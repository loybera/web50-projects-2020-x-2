document.addEventListener('DOMContentLoaded', () => {
 
            // Initialize new request
            const request = new XMLHttpRequest();
            const isbn = document.querySelector('#isbn').value;
            request.open('POST', '/reviewApi');
    
            // Callback function for when request completes
            request.onload = () => {
    
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);
    
                // Update the result div
                if (data.success) {
                    document.querySelector('#goodreads').innerHTML = `<h4>Reviews Count : ${data.review["work_ratings_count"]}</h4><h4>Average Rating: ${data.review["average_rating"]}</h4>` ;
                    // document.querySelector('#result').innerHTML = 'Api OK.';

                }
                else {
                    document.querySelector('#goodreads').innerHTML = `<h4>there is not stats.</h4>` ;
                    document.querySelector('#result').innerHTML = 'API Nok: There was an error.';
                }
            }
            // Add data to send with request
            const data = new FormData();
            data.append('isbn', isbn);
    
            // Send request
            request.send(data);
            return false;
        
    
});
    
 
  