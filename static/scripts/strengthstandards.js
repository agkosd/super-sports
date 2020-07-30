////////////////////////////////////////////////////////////////////
// Used with the StrengthStandards page in strengthstandards.html //
///////////////////////////////////////////////////////////////////

//Uses the brzycki equation to calculate 1RM
//https://en.wikipedia.org/wiki/One-repetition_maximum
function calcORM(weight, numReps){
	return (Math.floor(weight / ( 1.0278 - (0.0278 * numReps))))	;
}

//get the HTML elements from the page, which will be manipulated

//1RM calculator elements
var weightSlider = document.getElementById("weight-range");
var repSlider = document.getElementById("rep-range");
var weightText = document.getElementById("w-range-text");
var repText = document.getElementById("r-range-text");
var output = document.getElementById("1RM-result");
output.innerHTML = calcORM(parseInt(weightSlider.value), parseInt(repSlider.value));
var output2 = document.getElementById("1RM-result-Lb");
output2.innerHTML = calcORM(Math.floor(parseInt(weightSlider.value)* 2.204623), parseInt(repSlider.value) );

//variables for the correct functionality of the 1RM calculator
const MAX_REP = 20;
const MAX_WEIGHT = 300;


//This function changes the KG or LB text next to the weight text input slider in the 1RM calculator
function toggleUnit(){
	var unit = document.getElementById("unit-option-kg");
	var span = document.getElementById('1RM-unit-toggle');
	msg = unit.checked ? "(lbs)" : "(kgs)";
	span.innerHTML = msg;
}


//Manipulates the DOM based on the weight input slider in the 1RM calculator in the StrengthStandards page
weightSlider.oninput = function() {

	//calculates the output of the 1RM inputs specified by the weight and rep sliders
	output.innerHTML = calcORM(parseInt(this.value), parseInt(repSlider.value));
	output2.innerHTML = calcORM(Math.floor(parseInt(this.value)* 2.204623), parseInt(repSlider.value));

	//defines the unit multiplier based on the option selected in the KG/Lb toggle button
	var kg = document.getElementById("unit-option-kg");
	var unitMultiplier = kg.checked ? 1 : 2.204623;

	//displays the correct value representing the slider value in the text input box corresponding to the weight slider
	weightText.value = (Math.floor(parseInt(this.value)*unitMultiplier)).toString();

}

//Manipulates the DOM based on the reps input slider in the 1RM calculator in the StrengthStandards page
repSlider.oninput = function() {
	//calculates the 1RM output based on the 1RM inputs specified by the weight and rep sliders
	output.innerHTML = calcORM(parseInt(weightSlider.value), parseInt(this.value));
	output2.innerHTML = calcORM(Math.floor(parseInt(weightSlider.value)* 2.204623), parseInt(this.value));

	//displays the correct value representing the slider value in the text input box corresponding to the rep slider
	repText.value = this.value;
}

//Manipulates the DOM based on the  1RM calculator's weight input text box in the StrengthStandards page
//changes the slider to represent the text displayed in the text input box
weightText.onchange = function() {
	var unit = document.getElementById("unit-option-kg");
	//value entered in the text box
	var inputWeight = this.value;

	//the maximum weight the user can input is dependent on whether KG or LB are selected in the unit toggle button
	var maxWeightAdjusted = unit.checked ? MAX_WEIGHT : Math.floor(MAX_WEIGHT * 2.204623);

	//sets the adjusted weight from the user input to make it fit within the slider range of 0 to 300.
	//this is needed when pounds are selected because 1RM is calculated based on KGs
	var adjustedWeight = 0;
	//if pounds are selected as the unit of measurement, convert to KG so that it is valid in the slider range
	adjustedWeight = unit.checked ? parseInt(this.value) : Math.floor(parseInt(this.value) / 2.204623);


	console.log(MAX_WEIGHT + " " + inputWeight + " " + maxWeightAdjusted);

	//if input weight is greater than 300 (or 660 if LBs are chosen), adjust slider to maximum value
	//set text box to maximum value too 
	if (inputWeight > maxWeightAdjusted){
		adjustedWeight = MAX_WEIGHT;
		this.value = maxWeightAdjusted;
	
	//if input weight is less than 0, change slider and text values to 0
	} else if (parseInt(this.value) < 0 || this.value == ""){
		this.value = "0";
		adjustedWeight = "0";

	//otherwise set the text value to the inputted value
	} else {
		this.value = inputWeight;
	}

	//calculate the 1RM output based on the inputs (converted to kilograms) and output it
	output.innerHTML = calcORM(adjustedWeight, parseInt(repSlider.value));

	//change the slider valye to reflect the text input value
	weightSlider.value = adjustedWeight;

}


repText.onchange = function() {
	//if the text input value is greater than 20 or less than 0, set it to a value that is in the the specified slider range.
	if (parseInt(this.value) > MAX_REP){
		this.value = MAX_REP.toString();
	} else if (parseInt(this.value) <0 || this.value == ""){
		this.value = "0";
	}
	output.innerHTML = calcORM(parseInt(weightSlider.value), parseInt(this.value));
	//change the slider value
	repSlider.value = this.value;
}

//output to console the exercise selected from the dropdown menu
function refreshSelectedEx(){
	console.log("Exercise Changed");

}


//A list of multipliers for generating the strength standards for each exercise and each weight class
const BENCH_STANDARDS = [1.83, 0.37, 0.48, 0.59, 0.8];
const DL_STANDARDS = [2.96, 0.27, 0.5, 0.58, 0.8];
const SQUAT_STANDARDS = [2.58, 0.28, 0.46, 0.56, 0.76];
const OHP_STANDARDS = [1.14, 0.37, 0.51, 0.64, 0.77];

//generate the standard based on the chosen exercise, bodyweight and the standards category (novice, beginner, advanced, etc...)
function findStandard(column, bodyweight, exerciseType){

	//check whether kg or lbs are selected as unit of measurement
	var kg = document.getElementById("unit-option-kg");
	var unitMultiplier = kg.checked ? 1 : 2.204623;

	//find the maximum 1RM weight that can be lifted for a person with the specified bodyweight
	var maxWeight = exerciseType[0] * bodyweight * unitMultiplier;

	//Apply the multiplier for each standards category
	if (column == 1){
		return Math.floor(maxWeight * exerciseType[1] );
	} else if (column == 2){
		return Math.floor(maxWeight * exerciseType[2] );
	} else if (column == 3){
		return Math.floor(maxWeight * exerciseType[3] );
	}else if (column == 4){
		return Math.floor(maxWeight * exerciseType[4] );
	}

	//for the last column and category "Elite", output the maxWeight that was calculated.
	return Math.floor(maxWeight);

}

