
document.addEventListener('DOMContentLoaded', () => {
 
            var checkbox = document.getElementById("checkGetAPI") ;
            if (checkbox.checked){ 
                // Initialize new request
                var elementList = document.getElementsByClassName("isbnGridItem");
                var result = document.getElementById("result");
        
                // Primero, verifiquenmos que el párrafo tiene algún atributo    
                if (elementList.length>0) {
                //   var attrs = paragraph.attributes;
                var output = "";
                for(var i = elementList.length - 1; i >= 0; i--) {
                    api(elementList[i].value);
                }
                
                document.querySelector('#result').innerHTML ="fin de stats"
                } else {
                    document.querySelector('#result').innerHTML = "No hay atributos que mostrar";
                }
            }
 });

function api(id){
            const request = new XMLHttpRequest();
            const isbn = id

            request.open('POST', '/reviewApi');
    
            // Callback function for when request completes
            request.onload = () => {
    
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);
    
                // Update the result div
                if (data.success) {
                    document.querySelector('#goodreads'+id).innerHTML = `<h4>Reviews Count : ${data.review["work_ratings_count"]}</h4><h4>Average Rating: ${data.review["average_rating"]}</h4>` ;
                    document.querySelector('#result').innerHTML = 'Api OK.';

                }
                else {
                    document.querySelector('#goodreads'+id).innerHTML = `<h4>there is not stats.</h4>` ;
                    document.querySelector('#result').innerHTML = 'API Nok: There was an error.';
                }
            }
            // Add data to send with request
            const data = new FormData();
            data.append('isbn', isbn);
    
            // Send request
            request.send(data);
            return false;
        
    
    }
    
 
  