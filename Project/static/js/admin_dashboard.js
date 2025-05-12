let globalID=0
let baseUrl = new URL(window.location.href);
baseUrl = `${baseUrl.protocol}//${baseUrl.hostname}:${baseUrl.port}`;
function myshowLoader() {
    document.querySelector('.loader-wrapper').style.display = 'flex';
}
    
function myhideLoader() {
    document.querySelector('.loader-wrapper').style.display = 'none';
}

function showToastMessage(type, text) {
    switch (type) {
        case 'success':
            toastr.success(text);
            break;
        case 'info':
            toastr.info(text);
            break;
        case 'error':
            toastr.error(text);
            break;
        case 'warning':
            toastr.warning(text);
            break;
        default:
            console.error('Invalid toast type');
            break;
    }
}



function validateImageDimensions(file, callback) {
    const img = new Image();
    img.onload = function() {
        if (img.width === 1000 && img.height === 1000) {
            callback(true);
        } else {
            callback(false);
        }
    };
    img.onerror = function() {
        callback(false);
    };
    img.src = URL.createObjectURL(file);
}

$('#machineImageUploader').on('change', function(event) {
    var file = event.target.files[0];
    if (!file) {
        return;
    }
    
    validateImageDimensions(file, function(isValid) {
        if (!isValid) {
            showToastMessage("error", "Image dimensions must be 1000px by 1000px.")
            return;
        }
        
        var formData = new FormData();
        formData.append('file_doc', file);
    
        axios({
            method: 'POST',
            url: baseUrl + '/uploadFile',
            data: formData,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(res => {
            console.log(res.data);
            const responseData = res.data;  
            const uploadFilename = responseData.filename;
            console.log(uploadFilename);
      
            $('#machine_icon').attr('src', responseData.file_base64);
        
        }).catch(err => {
            console.error("Upload failed:", err);
            showToastMessage("error","Upload failed!")
            
        });
    });
});
function loadCategories() {
    myshowLoader();
    $.ajax({
        url: '/get_categories',
        method: 'GET',
        success: function(response) {
            $('#mycategory').empty();  // Clear the existing options
            response.forEach(function(category) {
                $('#mycategory').append(new Option(category.name, category.id));
            });
        },
        error: function(error) {
            console.error('Error fetching categories:', error);
        }
    });
    myhideLoader();
}




$(document).on('click', "#add_machine", function() {
    myshowLoader();
    
    // Get values from form
    let img_icon = $('#machine_icon').attr('src');
    let machine_name = ($('#machine_name').val() || "").trim();
    let machine_code = ($('#machine_code').val() || "").trim();
    let machine_secret = ($('#machine_secret').val() || "").trim();
    let machine_desc = ($('#machine_desc').val() || "").trim();
    
    // Check if machine image is the default image (i.e., not changed by the user)
    if (img_icon === 'https://dl5hm3xr9o0pk.cloudfront.net/instagram/p-details-big.jpg') {
        showToastMessage('error', 'Please upload a machine image!');
        myhideLoader();
        return;
    }

    // Validate required fields
    if (!machine_name || !machine_code || !machine_secret) {
        showToastMessage('error', 'Please fill in all required fields!');
        myhideLoader();
        return;
    }

    axios({
        method: 'POST',
        url: baseUrl + '/admin/create',
        data: {
            img_icon: img_icon,
            machine_name: machine_name,
            machine_code: machine_code,
            machine_secret: machine_secret,
            machine_desc: machine_desc
        }  
    }).then(res => {
        const response = res.data;
        console.log(response);
        if(response.status !== 200) {
            showToastMessage('error', 'Something Went Wrong!');
            myhideLoader();
            return;
        }
        showToastMessage('success', 'Successfully Added Machine!');
        location.reload(true);
    }).catch(err => {
        myhideLoader();
        console.log(err);
        showToastMessage('error', 'Something Went Wrong!');
    });
});



function getAllCustomfield() {
    var options = {};

    // Loop through each CustomFields div and collect data
    $('.CustomFields').each(function() {
        // Extract label text, removing any trailing colon and whitespace
        var label = $(this).find('.label_title').text().trim().replace(/:$/, '').trim();
        // Extract value from input field with class 'label_value'
        var price = $(this).find('.label_value').val();

        // Check if both label and price are valid
        if (label && price !== '') {
            options[label] = parseFloat(price);
        }
    });

    var result = {
        option: options
    };

    console.log(result);  // Log the result to the console
    return result;
}
$('#customfieldForm').on('click', '.btn', function(event) {
    event.preventDefault(); // Prevent the form from submitting (if it's inside a form)
    
    // Remove the parent div with the class 'CustomFields'
    $(this).closest('.CustomFields').remove();
});

$(document).on('click', "#updatebtn", function() {
    var id = $(this).attr('data-id');
    console.log("value ",id);
    axios({
        method: 'GET',
        url: baseUrl + `/admin/get/${id}` 
    }).then(res => {
        const response = res.data;
        console.log(response)
        globalID=response.id;
            
        $('#machine_icon').attr('src',response.machine_profile_img);
        $('#machine_name').val(response.machine_name);
        $('#machine_code').val(response.machine_code);
        $('#machine_secret').val(response.machine_password);
        $('#machine_desc').val(response.machine_description);
        $('#rndfk').click();
       
    }).catch(err => {
        myhideLoader();
        console.log(err)
        showToastMessage('error', 'Something Went Wrong!');
    });    
    

});

$(document).on('click', "#deletebtn", function() {
    var id = $(this).attr('data-id');
    console.log("value ", id);
    
    Swal.fire({
        title: "Are you sure?",
        text: "Product will permanently deleted!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d10000",
        cancelButtonColor: "#212529",
        confirmButtonText: "Yes, delete it!"
  }).then((result) => {
    if (result.isConfirmed) {
            axios({
                method: 'DELETE',
                url: baseUrl + `/admin/delete/${id}` 
            }).then(res => {
                const response = res.data;
                console.log(response);
                if (response.status !== 200) {
                    showToastMessage('error', response.message);
                    myhideLoader();
                    return;
                }
                showToastMessage('success', response.message);
                location.reload(true);
            }).catch(err => {
                myhideLoader();
                console.log(err);
                showToastMessage('error', 'Something Went Wrong!');
            });
        }
    });
});

$(document).on('click', "#update_machine", function() {
    myshowLoader();
    
    let img_icon = $('#machine_icon').attr('src');
    let machine_name = $('#machine_name').val().trim();
    let machine_code = $('#machine_code').val().trim();
    let machine_secret = $('#machine_secret').val().trim();
    let machine_desc = $('#machine_desc').val().trim();
    
    // Check if machine image is the default image (i.e., not changed by the user)
    if (img_icon === 'https://dl5hm3xr9o0pk.cloudfront.net/instagram/p-details-big.jpg') {
        showToastMessage('error', 'Please upload a machine image!');
        myhideLoader();
        return;
    }

    // Validate required fields
    if (!machine_name || !machine_code || !machine_secret) {
        showToastMessage('error', 'Please fill in all required fields!');
        myhideLoader();
        return;
    }

    axios({
        method: 'PUT',
        url: baseUrl + '/admin/create',
        data: {
            
            id: globalID,
            img_icon: img_icon,
            machine_name: machine_name,  
            machine_code: machine_code,
            machine_secret: machine_secret,
            machine_desc: machine_desc
        }  
    }).then(res => {
        const response = res.data;
        console.log(response);
        if(response.status !== 200) {
            showToastMessage('error', 'Something Went Wrong!');
            myhideLoader();
            return;
        }
        showToastMessage('success', 'Successfully Updated Machine!');
        location.reload(true);
    }).catch(err => {
        myhideLoader();
        console.log(err);
        showToastMessage('error', 'Something Went Wrong!');
    });
});

