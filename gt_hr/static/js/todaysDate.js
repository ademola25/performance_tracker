$(function() {
     $('.date-picker').datepicker(
                    {
                        dateFormat: "mm/yy",
                        changeMonth: true,
                        changeYear: true,
                        showButtonPanel: true,
                        onClose: function(dateText, inst) {
                        }
     
                    }

     )
                })