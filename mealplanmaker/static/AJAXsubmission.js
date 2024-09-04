// JavaScript for AJAX submission
function submitMealForm(dayId) {
    var form = $('#' + dayId);
    var url = form.attr('action');

    $.ajax({
        type: 'POST',
        url: url,
        data: form.serialize(),
        success: function(data) {
            console.log('Meal added successfully');
            // Update the UI as needed
        },
        error: function(xhr, status, error) {
            console.error('Error adding meal:', error);
        }
    });
}