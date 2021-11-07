const nationalIDField = document.querySelector('#nationalIDField');
const nationalIDFeedbackField = document.querySelector('.invalid_feedback');
const nationalIDSuccessOutput = document.querySelector(".nationalIDSuccessOutput");
const submitBtn = document.querySelector(".submit-btn");



nationalIDField.addEventListener('keyup',(e)=>{
    console.log(e.target.value);
    const nationalIDValue = e.target.value;
    nationalIDField.classList.remove("is-valid");
    nationalIDField.classList.remove("is-invalid");
    nationalIDFeedbackField.style.display = 'none';
    
    if (nationalIDValue.length>0){
        nationalIDSuccessOutput.style.display = 'block';
        nationalIDSuccessOutput.textContent = `checking ${nationalIDValue}`;

        fetch("/donors/donations/validate-donor", {
            body: JSON.stringify({ national_id: nationalIDValue }),
            method: "POST",
            headers : { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }).then((response) => response.json())
        .then((data) => {
            nationalIDSuccessOutput.style.display = 'none';

            if(data.national_id_error){
                nationalIDField.classList.add("is-invalid");
                nationalIDFeedbackField.style.display = 'block';
                nationalIDFeedbackField.innerHTML = `<p class="mx-3">${data.national_id_error}</p>`;
                submitBtn.disabled = true;
            } else {
                nationalIDField.classList.add("is-valid");
                submitBtn.removeAttribute("disabled");
            }
        }).catch(error => {console.error(error);});
    }else{
        nationalIDSuccessOutput.style.display = 'none';
    }
})