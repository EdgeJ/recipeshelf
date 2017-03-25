var room = 1;
function ingredient_fields() {
  room++;
  var objTo = document.getElementById('ingredient_fields')
  var divtest = document.createElement("div");
	divtest.setAttribute("class", "form-group removeclass"+room);
	var rdiv = 'removeclass'+room;
  divtest.innerHTML = '<div class="panel-body"> \
          <div id="ingredient_fields"></div> \
            <div class="col-sm-3 nopadding"> \
              <div class="form-group"> \
                <input type="text" class="form-control" id="Amount" name="Amount[]" value="" placeholder="Amount"> \
              </div> \
            </div> \
            <div class="col-sm-3 nopadding"> \
            <div class="form-group"> \
              <select class="form-control" id="Measure" name="Measure[]"> \
                <option value="">Measure</option> \
                <option value="C">C</option> \
                <option value="Tbsp">Tbsp</option> \
                <option value="tsp">tsp</option> \
              </select> \
            </div> \
          </div> \
          <div class="col-sm-3 nopadding"> \
            <div class="form-group"> \
              <div class="input-group"> \
                <input type="text" class="form-control" id="Ingredient" name="Ingredient[]" value="" placeholder="Ingredient"> \
                <div class="input-group-btn"> \
                  <button class="btn btn-danger" type="button" onclick="remove_ingredient_fields('+ room +');"> \
                    <span class="glyphicon glyphicon-minus" aria-hidden="true"></span> \
                  </button> \
                </div> \
              </div> \
            </div>';
  objTo.appendChild(divtest)
}

function remove_ingredient_fields(rid) {
 	$('.removeclass'+rid).remove();
}
