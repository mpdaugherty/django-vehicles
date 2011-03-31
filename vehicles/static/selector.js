var VEHICLE_ROOT = "/vehicles/";
jQuery(document).ready(function () {
    $("select.car-year-selector").change(function () {
	$.ajax({
	    url: VEHICLE_ROOT+this.value+"/makes",
	    context: this,
	    dataType: 'json',
	    success: function(data, status, xhr) {
		var $makeSelect = $(this).next("select.car-make-selector");
		$makeSelect.empty();
		for (var i=0; i<data.length; i++)
		{
		    $makeSelect.append($('<option value="'+data[i]+'">'+data[i]+'</option>'));
		}
		$makeSelect.change();
	    }
	});
    });
    $("select.car-make-selector").change(function () {
	$.ajax({
	    url: VEHICLE_ROOT+$(this).prev("select.car-year-selector").val()+"/"+this.value+"/models",
	    context: this,
	    dataType: 'json',
	    success: function(data, status, xhr) {
		var $makeSelect = $(this).next("select.car-model-selector");
		$makeSelect.empty()
		for (var i=0; i<data.length; i++)
		{
		    $makeSelect.append($('<option value="'+data[i].id+'">'+data[i].name+'</option>'));
		}
	    }
	});
    });
});