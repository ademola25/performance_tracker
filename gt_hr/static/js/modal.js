
$('#traineedeletModal').on('show.bs.modal', function (event) {
   
    var button = $(event.relatedTarget);
    var id = button.data('id');
    var name = button.data('name');
    $('#userForm').attr("action", "/hr-personnel/trainee-delete" + "/" + id);
    exampleModalLabel12.innerText = "Are you sure you want to Delete " + name + ' ?';
})



$('#hoddeletModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var id = button.data('id');
    var name = button.data('name');
    console.log(id, name)
    $('#hodDeleteForm').attr("action", "/hr-personnel/delete-user" + "/" + id);
    hodNameText.innerText = "Are you sure you want to Delete " + name + ' ?';
})


$('#managerdeletModal').on('show.bs.modal', function (event) {
    
    var button = $(event.relatedTarget);
    var id = button.data('id');
    var name = button.data('name');

    $('#managerDeleteForm').attr("action", "/hr-personnel/manager-delete" + "/" + id);

    manager.innerText = "Are you sure you want to Delete " + name + ' ?';
})


$('#departmentdeletModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var id = button.data('id');
    var name = button.data('name');
    $('#departmentDeleteForm').attr("action", "/hr-personnel/delete-department" + "/" + id);
    departmentModalTitle.innerText = "Are you sure you want to Delete " + name + ' ?';

})




$('#submitlog').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);


})