function readURL(input) {
    if (input[0].files && input[0].files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            input.nextAll('img')
                .attr('src', e.target.result)
                .attr('style', 'width: 500px;border: 1px solid black;')
                .show();
        };

        reader.readAsDataURL(input[0].files[0]);
    }
}