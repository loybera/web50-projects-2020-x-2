
    document.addEventListener('DOMContentLoaded', () => {
 
        var checkbox = document.getElementById("checkGetAPI");
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