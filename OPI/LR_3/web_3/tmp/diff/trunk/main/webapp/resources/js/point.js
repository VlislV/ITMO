let rInput = document.querySelector('#r_input');
let xInput = document.querySelector('#x_input');
let yInput = document.querySelector('#y_input');
let sub_btn = document.querySelector('#submit');
let point = document.querySelector('#point');
function setPoint(event){
    if (!point) {
        point = document.getElementById('point');
    }
    if (point) {
        point.setAttribute("cx", event.offsetX);
        point.setAttribute("cy", event.offsetY);
        point.setAttribute("visibility", "visible");
    }
    
    let rValue = parseFloat(rInput.value) || 2.0;
    let x = (event.offsetX - 150) / 100 * rValue;
    let y = (150 - event.offsetY) / 100 * rValue;
    let validX = [-2, -1, 0, 1, 2];
    let closestX = validX.reduce((prev, curr) => {
        return Math.abs(curr - x) < Math.abs(prev - x) ? curr : prev;
    });

    console.log(x, y);
    console.log("closest X:", closestX, "Y:", y.toFixed(10));

        yInput.value = y.toFixed(10);
        xInput.value = closestX;
        xInput.dispatchEvent(new Event('input', { bubbles: true }));
        yInput.dispatchEvent(new Event('input', { bubbles: true }));

        sub_btn.click();
}

document.addEventListener("DOMContentLoaded", function() {
    let figure = document.getElementById("fig");
    if (figure) {
        figure.addEventListener("click", setPoint);
    }
    if (rInput) {
    }
});