$(document).on('click', '#close-preview', function(){ 
    $('.image-preview').popover('hide');
    // Hover befor close the preview
    $('.image-preview').hover(
        function () {
           $('.image-preview').popover('show');
        }, 
         function () {
           $('.image-preview').popover('hide');
        }
    );    
});

$(function() {
    // Create the close button
    var closebtn = $('<button/>', {
        type:"button",
        text: 'x',
        id: 'close-preview',
        style: 'font-size: initial;',
    });
    closebtn.attr("class","close pull-right");
    // Set the popover default content
    $('.image-preview').popover({
        trigger:'manual',
        html:true,
        title: "<strong>Preview</strong>"+$(closebtn)[0].outerHTML,
        content: "There's no image",
        placement:'bottom'
    });
    // Clear event
    $('.image-preview-clear').click(function(){
        $('.image-preview').attr("data-content","").popover('hide');
        $('.image-preview-filename').val("");
        $('.image-preview-clear').hide();
        $('.image-preview-input input:file').val("");
        $(".image-preview-input-title").text("Browse"); 
    }); 
    // Create the preview image
    $(".image-preview-input input:file").change(function (){     
        var img = $('<img/>', {
            id: 'dynamic',
            width:250,
            height:200
        });      
        var file = this.files[0];
        var reader = new FileReader();
        // Set preview image into the popover data-content
        reader.onload = function (e) {
            $(".image-preview-input-title").text("Change");
            $(".image-preview-clear").show();
            $(".image-preview-filename").val(file.name);            
            img.attr('src', e.target.result);
            $(".image-preview").attr("data-content",$(img)[0].outerHTML).popover("show");
        }        
        reader.readAsDataURL(file);
    });  
});



    $(function () {

        $('#info-form-link').click(function (e) {
            $("#infoSection").delay(100).fadeIn(100);
            $("#multiSection").fadeOut(100);
			$("#toolSection").fadeOut(100);
            $('#multi-form-link').removeClass('active');
			$('#tools-form-link').removeClass('active');
            $(this).addClass('active');
            e.preventDefault();
        });
        $('#multi-form-link').click(function (e) {
            $("#multiSection").delay(100).fadeIn(100);
            $("#infoSection").fadeOut(100);
			$("#toolSection").fadeOut(100);
            $('#info-form-link').removeClass('active');
			$('#tools-form-link').removeClass('active');
            $(this).addClass('active');
            e.preventDefault();
        });
		$('#tools-form-link').click(function (e) {
            $("#toolSection").delay(100).fadeIn(100);
            $("#multiSection").fadeOut(100);
			$("#infoSection").fadeOut(100);
            $('#multi-form-link').removeClass('active');
			$('#info-form-link').removeClass('active');
            $(this).addClass('active');
            e.preventDefault();
        });

    });

	
	
	

    

// Profile image file upload
document.getElementById('profileImg-button-browse').addEventListener('click', function() {
	document.getElementById('files-input-upload').click();
});

document.getElementById('files-input-upload').addEventListener('change', function() {
	document.getElementById('profileImg-input-name').value = this.value;
	document.getElementById('profileImg-button-upload').removeAttribute('disabled');
});

function submitProfileImg()
{
	document.getElementById('profileImgForm').submit()
}


// 5 image file upload

document.getElementById('img-button-browse').addEventListener('click', function() {
	document.getElementById('5files-input-upload').click();
});

document.getElementById('5files-input-upload').addEventListener('change', function() {
	document.getElementById('img-input-name').value = this.value;
	document.getElementById('img-button-upload').removeAttribute('disabled');
});

function submitImg()
{
	document.getElementById('imgForm').submit()
}
	
	
	

	
	
	
    $(document).ready(function(){
        //FANCYBOX
        //https://github.com/fancyapps/fancyBox
        $(".fancybox").fancybox({
            openEffect: "none",
            closeEffect: "none"
        });
    });

$(document).ready(function() {
    $('#myCarousel').carousel({
	    interval: 10000
	})
});

$(document).ready(codeAddress());