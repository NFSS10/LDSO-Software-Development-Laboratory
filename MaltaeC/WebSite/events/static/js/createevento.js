$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});
$('#datepickerIni').datepicker({});
$('#datepickerFim').datepicker({});
$('#datepickerIni').datepicker()
  .on('changeDate',function(e){
    $('#datepickerFim').datepicker('setStartDate',e.date);
    var inp = document.getElementById("date_initial");
    var split = inp.value.split('T');
    var day = e.date.getDate()
    var month = e.date.getMonth() + 1
    var year = e.date.getFullYear()
    split[0] = year+'-'+month+'-'+day
    inp.value = split[0]+'T'+split[1];
  });
$('#datepickerIni').datepicker('setStartDate', new Date());
$('#datepickerFim').datepicker('setStartDate', new Date());
$('#datepickerFim').datepicker()
.on('changeDate',function(e){
  var inp = document.getElementById("date_final");
  var split = inp.value.split('T');
  var day = e.date.getDate()
  var month = e.date.getMonth() + 1
  var year = e.date.getFullYear()
  split[0] = year+'-'+month+'-'+day
  inp.value = split[0]+'T'+split[1];
});
$('#timepickerIni').timepicker({showMeridian: false})
$('#timepickerFim').timepicker({showMeridian: false})
document.getElementById("date_initial").value = "nullT"+document.getElementById("timepickerIni").value
document.getElementById("date_final").value = "nullT"+document.getElementById("timepickerFim").value
$('#timepickerIni').timepicker().on('changeTime.timepicker', function(e) {
  var inp = document.getElementById("date_initial");
  var split = inp.value.split('T');
  let hours;
  let minutes;
  minutes = /*e.time.minutes < 10 ? '0'+ e.time.minutes :*/ e.time.minutes;
  hours = /*e.time.hours < 10 ? '0'+ e.time.hours :*/ e.time.hours;
  split[1] = hours+':'+minutes
  inp.value = split[0]+'T'+split[1];
});
$('#timepickerFim').timepicker().on('changeTime.timepicker', function(e) {
  var inp = document.getElementById("date_final");
  var split = inp.value.split('T');
  let hours;
  let minutes;
  minutes = /*e.time.minutes < 10 ? '0'+ e.time.minutes :*/ e.time.minutes;
  hours = /*e.time.hours < 10 ? '0'+ e.time.hours :*/ e.time.hours;
  split[1] = hours+':'+minutes
  inp.value = split[0]+'T'+split[1];
});
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
var csrftoken = getCookie('csrftoken');
parseAndLoadDates = function(i, f){
  var split = i.split('T');
  var stime = split[1].split(':');
  var ptime;
  if(Number(stime[0]) > 12){
    ptime = String(Number(stime[0]) % 12)+':'+stime[1]+' PM'
  }else{
    ptime = stime[0]+':'+stime[1]+' AM'
  }
  document.getElementById("timepickerIni").value = ptime;
  var r = split[0].split('-');
  var rr = r[1]+'-'+r[2]+'-'+r[0]
  $('#datepickerIni').data({date: rr});
  $('#datepickerIni').datepicker('update');
  $('#datepickerIni').datepicker().children('input').val(rr);
  split = f.split('T');
  stime = split[1].split(':');
  if(Number(stime[0]) > 12){
    ptime = String(Number(stime[0]) % 12)+':'+stime[1]+' PM'
  }else{
    ptime = stime[0]+':'+stime[1]+' AM'
  }
  document.getElementById("timepickerFim").value = ptime;
  var s = split[0].split('-');
  var ss = s[1]+'-'+s[2]+'-'+s[0]
  $('#datepickerFim').data({date: ss});
  $('#datepickerFim').datepicker('update');
  $('#datepickerFim').datepicker().children('input').val(ss);
  console.log(f);
}
/*GOOGLE MAPS API*/
var map
var editLat = null
var editLon = null
let placeSearch, autocomplete;
let componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};
var initMap = function(){
  let porto
  if(window.location.pathname.includes("editar")){
    porto = {lat: editLat, lng: editLon};
    document.getElementById("latitude").value=Number(editLat)
    document.getElementById("longitude").value=Number(editLon)
  }
  else
    porto = {lat: 41.1496100, lng:  -8.6109900};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 9,
    center: {lat: porto.lat, lng: porto.lng}
  });
  var marker = new google.maps.Marker({
    position: porto,
    map: map
  });
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {!HTMLInputElement} */(document.getElementById('local')),
      {types: ['geocode']});
  autocomplete.bindTo('bounds', map);
  autocomplete.addListener('place_changed', function() {
          marker.setVisible(false);
          var place = autocomplete.getPlace();
          if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
          }

          // If the place has a geometry, then present it on a map.
          if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
          } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);  // Why 17? Because it looks good.
          }
          marker.setPosition(place.geometry.location);
          document.getElementById("longitude").value = place.geometry.location.lng();
          document.getElementById("latitude").value = place.geometry.location.lat();
          marker.setVisible(true);

          var address = '';
          if (place.address_components) {
            address = [
              (place.address_components[0] && place.address_components[0].short_name || ''),
              (place.address_components[1] && place.address_components[1].short_name || ''),
              (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
          }
        });

}
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}
/*GOOGLE MAPS API END*/
/*CAROUSEL JAVASCIPT*/
let timeDelay = 0;
function manageCarousel(e){
  if(new Date().getTime() - timeDelay > 1000 ){
    var op = e.target.attributes["id"].value.split("pager")[1]
    var index = $(".active").index()
    var buttons = document.getElementById("pager").children
    switch (op) {
      case "Next":
        if(index < 3){
            $("html, body").animate({ scrollTop: 0 }, "slow");
            $("#formCarousel").carousel("next");
        }
        if(index == 0){
          buttons[0].classList.remove("disabled")
          google.maps.event.trigger(map, 'resize');
        }else if(index == 2){
          buttons[1].classList.add("disabled")
        }
        break;
      case "Prev":
      if(index > 0){
          $("html, body").animate({ scrollTop: 0 }, "slow");
          $("#formCarousel").carousel("prev");
      }
      if(index == 3){
        buttons[1].classList.remove("disabled")
      }else if(index == 1){
        buttons[0].classList.add("disabled")
      }
        break;
      default:

    }
    timeDelay = new Date().getTime();
  }

}
if(document.getElementById("pagerPrev") != null)
    document.getElementById("pagerPrev").onclick = manageCarousel
if(document.getElementById("pagerNext") != null)
    document.getElementById("pagerNext").onclick = manageCarousel
/*CAROUSEL JAVASCIPT END*/
var countTutors = 0;
function removetutor(id){
  $("#li"+id).remove();
  let list = document.getElementById("selectedTutors").getElementsByTagName("li");
  let stringValue = '';
  for(var i = 0; i < list.length; i++){
    let text = list[i].innerText;
    text = text.substring(0,text.length - 1);
    stringValue = stringValue + ";" + text;
  }
  document.getElementById("listTutor").value = stringValue.substring(1);
  document.getElementById("listTutor").value = document.getElementById("listTutor").value.replace(/\r?\n?/g, '')
  if(list.length == 0){
    $("#selectedTutors").append('<li id="placeholderli" style="color: rgb(128,128,128)" class="list-group-item">Use a caixa de texto acima para colocar nomes</li>');
  }
}
function addtutor(e){
  let tutor = document.getElementById("tutor");
  if(tutor.value.length > 0){
    $("#selectedTutors").append('<li id=li'+countTutors+' class="list-group-item">'+tutor.value+'<a onclick=removetutor('+countTutors+') class="badge">&times;</a></li>');
    countTutors++;
    tutor.value = "";
    let list = document.getElementById("selectedTutors").getElementsByTagName("li");
    if(list[0].attributes.id.value == "placeholderli"){
      $("#placeholderli").remove()
      list = document.getElementById("selectedTutors").getElementsByTagName("li");
    }
    let stringValue = '';
    for(var i = 0; i < list.length; i++){
      let text = list[i].innerText;
      text = text.substring(0,text.length - 1);
      stringValue = stringValue + ";" + text;
    }
    document.getElementById("listTutor").value = stringValue.substring(1);
    document.getElementById("listTutor").value = document.getElementById("listTutor").value.replace(/\r?\n?/g, '')
  }
}
document.getElementById("tutorButtonAdd").onclick = addtutor
document.getElementById("tutor").onkeydown = function(e){
  if(e.code == "Enter"){
    addtutor(e)
    e.preventDefault();
  }
}
//dropzone
function initImageUpload(box) {
  let uploadField = box.querySelector('.image-upload');

  uploadField.addEventListener('change', getFile);

  function getFile(e){
    let file = e.currentTarget.files[0];
    checkType(file);
  }

  function previewImage(file){
    let thumb = box.querySelector('.js--image-preview'),
        reader = new FileReader();

    reader.onload = function() {
      thumb.style.backgroundImage = 'url(' + reader.result + ')';
    }
    reader.readAsDataURL(file);
    thumb.className += ' js--no-default';
  }

  function checkType(file){
    let imageType = /image.*/;
    if (!file.type.match(imageType)) {
      throw 'Datei ist kein Bild';
    } else if (!file){
      throw 'Kein Bild gewählt';
    } else {
      previewImage(file);
    }
  }

}
// initialize box-scope
var boxes = document.querySelectorAll('.box');

for(let i = 0; i < boxes.length; i++) {//if (window.CP.shouldStopExecution(1)){break;}
  let box = boxes[i];
  initDropEffect(box);
  initImageUpload(box);
}
/// drop-effect
function initDropEffect(box){
  let area, drop, areaWidth, areaHeight, maxDistance, dropWidth, dropHeight, x, y;

  // get clickable area for drop effect
  area = box.querySelector('.js--image-preview');
  area.addEventListener('click', fireRipple);

  function fireRipple(e){
    area = e.currentTarget
    // create drop
    if(!drop){
      drop = document.createElement('span');
      drop.className = 'drop';
      this.appendChild(drop);
    }
    // reset animate class
    drop.className = 'drop';

    // calculate dimensions of area (longest side)
    areaWidth = getComputedStyle(this, null).getPropertyValue("width");
    areaHeight = getComputedStyle(this, null).getPropertyValue("height");
    maxDistance = Math.max(parseInt(areaWidth, 10), parseInt(areaHeight, 10));

    // set drop dimensions to fill area
    drop.style.width = maxDistance + 'px';
    drop.style.height = maxDistance + 'px';

    // calculate dimensions of drop
    dropWidth = getComputedStyle(this, null).getPropertyValue("width");
    dropHeight = getComputedStyle(this, null).getPropertyValue("height");

    // calculate relative coordinates of click
    // logic: click coordinates relative to page - parent's position relative to page - half of self height/width to make it controllable from the center
    x = e.pageX - this.offsetLeft - (parseInt(dropWidth, 10)/2);
    y = e.pageY - this.offsetTop - (parseInt(dropHeight, 10)/2) - 30;

    // position drop and animate
    drop.style.top = y + 'px';
    drop.style.left = x + 'px';
    drop.className += ' animate';
    e.stopPropagation();

  }
}
//Funções helper para edit
function setUpTutors(tut){
  $("#selectedTutors").append('<li id=li'+countTutors+' class="list-group-item">'+tut+'<a onclick=removetutor('+countTutors+') class="badge">&times;</a></li>');
  countTutors++;
  tutor.value = "";
  let list = document.getElementById("selectedTutors").getElementsByTagName("li");
  if(list[0].attributes.id.value == "placeholderli"){
    $("#placeholderli").remove()
    list = document.getElementById("selectedTutors").getElementsByTagName("li");
  }
  let stringValue = '';
  for(var i = 0; i < list.length; i++){
    let text = list[i].innerText;
    text = text.substring(0,text.length - 1);
    stringValue = stringValue + ";" + text;
  }
  document.getElementById("listTutor").value = stringValue.substring(1);
}
function setUpCalendar(di,df,hi,hf){
  let el = di.split('-')
  let d = new Date(el[0],Number(el[1])-1, el[2])
  $('#datepickerIni').datepicker('setDate',d);
  el = df.split('-')
  d = new Date(el[0],Number(el[1])-1, el[2])
  $('#datepickerFim').datepicker('setDate',d);
  document.getElementById("timepickerIni").value = hi
  document.getElementById("timepickerFim").value = hf
  let inp = document.getElementById("date_initial");
  let hours;
  let minutes;
  el = inp.value.split('T');
  minutes = hi.split(':')[1];
  hours = hi.split(':')[0];
  el[1] = hours+':'+minutes
  inp.value = el[0]+'T'+el[1];
  inp = document.getElementById("date_final");
  el = inp.value.split('T');
  minutes = hf.split(':')[1];
  hours = hf.split(':')[0];
  el[1] = hours+':'+minutes
  inp.value = el[0]+'T'+el[1];
}
