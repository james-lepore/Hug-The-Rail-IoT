var suggestionVal = 0;

$(document).ready(function() {
	try {
		var u = document.getElementById("uname");
		var p = document.getElementById("psw");
		
		u.addEventListener("keyup", function(event) {
			if (event.key == "Enter") {
				event.preventDefault();
				document.getElementById("login_button").click();
			}
		});

		p.addEventListener("keyup", function(event) {
			if (event.key == "Enter") {
				event.preventDefault();
				document.getElementById("login_button").click();
			}
		});
	} catch {}
});

function login() {
	$.ajax({
		data : {
		  usr : document.getElementById("uname").value,
		  pwd : document.getElementById("psw").value
		},
		type : 'POST',
		url : '/login'
	}).done(function(data) {
		if(data == "Login Failed. Please Try Again."){
			alert(data);
		} else {
			window.location.href = '/'+data
		}
	});
}

function logoff() {
	window.location.href = "/"
}

function start_trip() {
	document.getElementById("start_trip").style.pointerEvents = "none";
	document.getElementById("start_trip").style.opacity = "0.6";
	$.ajax({
		type : 'POST',
		url : '/operator'
	}).done(function(duration) {
		dur = parseInt(duration, 10);
		myLoop(dur);
	});
}

function myLoop(dur) {
	setTimeout(function() {  		 	
		$.ajax({
			data : {
			  speed : document.getElementById("speed_val").value,
			},
			type : 'POST',
			url : '/operator/trip'
		}).done(function(data) {
			if(dur == 0){
				reset();
				return;
			}
			data = data.split(",");

			console.log(dur, data);

			set(data);
		});
		dur--;                  
		if (dur > 0) {           
		  myLoop(dur);       
		} else {
			alert("trip over");
		}  
	  }, 500);
}

function set(data){
	//Rain
	document.getElementById("rain_val").innerHTML = data[13] + " IN";
	if(data[1] == 'ok') {
		document.getElementById("rain_ok").style.display = "block";
		document.getElementById("rain_hazard").style.display = "none";
		document.getElementById("rain_warning").style.display = "none";
	} else if (data[1] == 'hazard'){
		document.getElementById("rain_ok").style.display = "none";
		document.getElementById("rain_hazard").style.display = "block";
		document.getElementById("rain_warning").style.display = "none";
	} else {
		document.getElementById("rain_ok").style.display = "none";
		document.getElementById("rain_hazard").style.display = "none";
		document.getElementById("rain_warning").style.display = "block";
	}

	//Wind
	document.getElementById("wind_val").innerHTML = data[14] + " MPH"
	if(data[3] == 'ok') {
		document.getElementById("wind_ok").style.display = "block";
		document.getElementById("wind_hazard").style.display = "none";
		document.getElementById("wind_warning").style.display = "none";
	} else if (data[3] == 'hazard'){
		document.getElementById("wind_ok").style.display = "none";
		document.getElementById("wind_hazard").style.display = "block";
		document.getElementById("wind_warning").style.display = "none";
	} else {
		document.getElementById("wind_ok").style.display = "none";
		document.getElementById("wind_hazard").style.display = "none";
		document.getElementById("wind_warning").style.display = "block";
	}
	
	//Slip
	document.getElementById("slip_val").innerHTML = data[15] + " RPM difference"
	if(data[5] == 'ok') {
		document.getElementById("slip_ok").style.display = "block";
		document.getElementById("slip_hazard").style.display = "none";
		document.getElementById("slip_warning").style.display = "none";
	} else if (data[5] == 'hazard'){
		document.getElementById("slip_ok").style.display = "none";
		document.getElementById("slip_hazard").style.display = "block";
		document.getElementById("slip_warning").style.display = "none";
	} else {
		document.getElementById("slip_ok").style.display = "none";
		document.getElementById("slip_hazard").style.display = "none";
		document.getElementById("slip_warning").style.display = "block";
	}

	//Stationary Object Detection
	document.getElementById("stat_val").innerHTML = (data[9] == "ok" ? 'No' : (data[9] == "hazard" ? 'Calculating...' : data[16] + "M away"))
	if(data[9] == 'ok') {
		document.getElementById("stat_ok").style.display = "block";
		document.getElementById("stat_hazard").style.display = "none";
		document.getElementById("stat_warning").style.display = "none";
	} else if (data[9] == 'hazard'){
		document.getElementById("stat_ok").style.display = "none";
		document.getElementById("stat_hazard").style.display = "block";
		document.getElementById("stat_warning").style.display = "none";
	} else {
		document.getElementById("stat_ok").style.display = "none";
		document.getElementById("stat_hazard").style.display = "none";
		document.getElementById("stat_warning").style.display = "block";
	}
	
	//Moving Object Detection
	document.getElementById("mov_val").innerHTML = (data[7] == "ok" ? 'No' : (data[7] == "hazard"? 'Calculating...' : data[16] + "M away"))
	if(data[7] == 'ok') {
		document.getElementById("mov_ok").style.display = "block";
		document.getElementById("mov_hazard").style.display = "none";
		document.getElementById("mov_warning").style.display = "none";
	} else if (data[7] == 'hazard'){
		document.getElementById("mov_ok").style.display = "none";
		document.getElementById("mov_hazard").style.display = "block";
		document.getElementById("mov_warning").style.display = "none";
	} else {
		document.getElementById("mov_ok").style.display = "none";
		document.getElementById("mov_hazard").style.display = "none";
		document.getElementById("mov_warning").style.display = "block";
	}

	//Closed Gate Detection
	document.getElementById("gate_val").innerHTML = (data[17] == "0" ? 'No' : 'Potential')
	if(data[11] == 'ok') {
		document.getElementById("gate_ok").style.display = "block";
		document.getElementById("gate_warning").style.display = "none";
	} else {
		document.getElementById("gate_ok").style.display = "none";
		document.getElementById("gate_warning").style.display = "block";
	}

	// Suggestion Value
	document.getElementById("suggestion").innerHTML = data[19];
	suggestionVal = parseInt(data[18], 10);
	if(data[19] == "---No Suggestion---"){
		document.getElementById("acc_sug").style.display = "none";
	} else {
		document.getElementById("acc_sug").style.display = "block";
	}
}

function accept_suggestion() {
	document.getElementById("speed_val").value = suggestionVal;
	document.getElementById("acc_sug").style.display = "none";
}

function reset() {
	document.getElementById("start_trip").style.pointerEvents = "auto";
	document.getElementById("start_trip").style.opacity = "1";
	document.getElementById("speed_val").value = 0;
	document.getElementById("suggestion").innerHTML = "---No Suggestion---";
	document.getElementById("acc_sug").style.display = "none";
	document.getElementById("rain_val").innerHTML = "N/A";
	document.getElementById("rain_ok").style.display = "none";
	document.getElementById("rain_hazard").style.display = "none";
	document.getElementById("rain_warning").style.display = "none";
	document.getElementById("wind_val").innerHTML = "N/A";
	document.getElementById("wind_ok").style.display = "none";
	document.getElementById("wind_hazard").style.display = "none";
	document.getElementById("wind_warning").style.display = "none";
	document.getElementById("slip_val").innerHTML = "N/A";
	document.getElementById("slip_ok").style.display = "none";
	document.getElementById("slip_hazard").style.display = "none";
	document.getElementById("slip_warning").style.display = "none";
	document.getElementById("stat_val").innerHTML = "N/A";
	document.getElementById("stat_ok").style.display = "none";
	document.getElementById("stat_hazard").style.display = "block";
	document.getElementById("stat_warning").style.display = "none";
	document.getElementById("mov_val").innerHTML = "N/A";
	document.getElementById("mov_ok").style.display = "none";
	document.getElementById("stat_hazard").style.display = "none";
	document.getElementById("mov_warning").style.display = "none";
	document.getElementById("gate_val").innerHTML = "N/A";
	document.getElementById("gate_ok").style.display = "none";
	document.getElementById("gate_warning").style.display = "none";
}

function tech_log() {
	document.getElementById("log_button").style.opacity = "0.6";
	document.getElementById("update_button").style.opacity = "0.6";
	document.getElementById("log_button").style.pointerEvents = "none";
	document.getElementById("update_button").style.pointerEvents = "none";
	$.ajax({
		type : 'POST',
		url : '/technician/log'
	}).done(function(data) {
		alert(data)
		document.getElementById("log_button").style.opacity = "1";
		document.getElementById("update_button").style.opacity = "1";
		document.getElementById("log_button").style.pointerEvents = "auto";
		document.getElementById("update_button").style.pointerEvents = "auto";
	});
}

function tech_update() {
	document.getElementById("log_button").style.opacity = "0.6";
	document.getElementById("update_button").style.opacity = "0.6";
	document.getElementById("log_button").style.pointerEvents = "none";
	document.getElementById("update_button").style.pointerEvents = "none";
	$.ajax({
		type : 'POST',
		url : '/technician/update'
	}).done(function(data) {
		alert(data)
		document.getElementById("log_button").style.opacity = "1";
		document.getElementById("update_button").style.opacity = "1";
		document.getElementById("log_button").style.pointerEvents = "auto";
		document.getElementById("update_button").style.pointerEvents = "auto";
	});
}
