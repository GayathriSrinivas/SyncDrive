$(function() {
	var drop = document.querySelector('#pane1');
	addEvent(drop, 'dragover', cancel);
	addEvent(drop, 'dragenter', cancel);
	addEvent(drop, 'drop', drophandler);
	drop = document.querySelector('#pane2');
	addEvent(drop, 'dragover', cancel);
	addEvent(drop, 'dragenter', cancel);
	addEvent(drop, 'drop', drophandler);
});

var paneDrive = [-1, -1];

function onDropDownSelect(id) {
	var pane = (id == "pane1_drive") ? '1' : '2';
	var drive = $('#' + id).val();
	listFiles(pane, drive, '');
}

function drophandler(event) {
	var text = event.dataTransfer.getData('Text');
	var srcId = text.substring(2);
	var src = parseInt(text.substring(1,2));
	var dst = (src == 1) ? 2 : 1;
	$.get('/transfer_file?src=' + paneDrive[src - 1] + '&dst=' + paneDrive[dst - 1] + '&file_id=' + srcId, function(data) {
		alert('success! ' + data);
	});
}

function cancel(event) {
    if (event.preventDefault) {
        event.preventDefault();
    }
    return false;
}

function listFiles(pane, drive, folder) {
	paneDrive[parseInt(pane) - 1] = drive;
	$('#drivePane' + pane).html('Please wait.. Fetching data..');
	$.get('/list_files?drive=' + drive + '&folder=' + folder + '&pane=' + pane , function(data) {
		$('#drivePane' + pane).html(data);
		makeDraggable();
	});
}

function makeDraggable() {
    var dragItems = document.querySelectorAll('a');
    for (var i = 0; i < dragItems.length; i++) {
        addEvent(dragItems[i], 'dragstart', function (event) {
        event.dataTransfer.setData('Text', this.id);
      });
    }
}