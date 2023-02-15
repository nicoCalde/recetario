/* Form_complex add and remove buttons */
document.addEventListener('click', (event)=>{
    if (event.target.id == 'add-more') {
        add_new_form(event)
    }
  });
  function add_new_form(event){
    if (event){
        event.preventDefault()
    }
    const totalNewForms = document.getElementById('id_form-TOTAL_FORMS')
    const currentIngredientForms = document.getElementsByClassName('ingredient-form')
    const currentFormCount = currentIngredientForms.length
    const valueCount = currentFormCount + 1
    const formCopyTarget = document.getElementById('ingredient-form-list')
    const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
    copyEmptyFormEl.setAttribute('class','ingredient-form')
    copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__','g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex,currentFormCount)
    totalNewForms.setAttribute('value',valueCount)
    formCopyTarget.append(copyEmptyFormEl) 
  };
  document.addEventListener('click', (event)=>{
    if (event.target.id == 'remove-one') {
        remove_last_form(event)
    }
  });
  function remove_last_form(event){
    if (event){
        event.preventDefault()
    }
    const totalForms = document.getElementById('id_form-TOTAL_FORMS')
    const currentIngredientForms = document.getElementsByClassName('ingredient-form')
    const currentFormCount = currentIngredientForms.length - 1
    const removeElParent = document.getElementById('ingredient-form-list')
    const removeElChild = document.getElementById(`form-${currentFormCount}`)
    removeElParent.removeChild(removeElChild)
    const valueCount = currentIngredientForms.length
    totalForms.setAttribute('value',valueCount)   
  };