function getSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
      result.push(opt.value || opt.text);
    }
  }
  var x=result[0];
  let e=document.getElementById("crafters");
  for(var i=1;i< result.length;i++){
  x=x+" "+result[i];
  }
  e.value=x;
  }