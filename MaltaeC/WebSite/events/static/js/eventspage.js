
var mc = function(e){
  var action = e.target.id;
  var input = document.getElementById("searchtype");
  switch (action) {
    case "cat":
      e.target.attributes.class.value = "btn btn-default";
      input.value = "cat";
      document.getElementById("dat").attributes.class.value = "btn btn-info";
      document.getElementById("loc").attributes.class.value = "btn btn-info";
      $('#catdiv').collapse("show");
      $('#datdiv').collapse("hide");
      $('#locdiv').collapse("hide");
      break;
    case "dat":
      e.target.attributes.class.value = "btn btn-default";
      input.value = "dat";
      document.getElementById("cat").attributes.class.value = "btn btn-info";
      document.getElementById("loc").attributes.class.value = "btn btn-info";
      $('#catdiv').collapse("hide");
      $('#datdiv').collapse("show");
      $('#locdiv').collapse("hide");
      break;
    case "loc":
      e.target.attributes.class.value = "btn btn-default";
      input.value = "loc";
      document.getElementById("cat").attributes.class.value = "btn btn-info";
      document.getElementById("dat").attributes.class.value = "btn btn-info";
      $('#catdiv').collapse("hide");
      $('#datdiv').collapse("hide");
      $('#locdiv').collapse("show");
      break;
    default:
      break;
  }
}
document.getElementById("cat").onclick = mc
document.getElementById("dat").onclick = mc
document.getElementById("loc").onclick = mc
// /* Função que vai fazer construir string com 4 primeiras palavras da descricao */
// function splitDescricao(id,description){
//    paragraph = document.getElementById(id+'paragraph');

//    if(description.length > 15){
//       var about = description.split(" ");
//       var splitmessage = "";
//       for (var i=0; i<4; i++){
//          splitmessage += about[i] + " ";
//       }

//       splitmessage += "(...)";
//       paragraph.append(splitmessage);
//    }else{
//       paragraph.append(description);
//    }
// }
