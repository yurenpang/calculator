$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/query",
        async: true
    }).done(function(data) {

        if(data.error) {
            alert("Cannot render data");
        } else {
            $("tbody").empty()

            alert("Hii")

            for(let i = 0; i < data.length; i++) {
                $("tbody").append("<tr>" +
                "<td>" + str(i) + "</td>" +
                "<td>" + data[i]['ip'] + "</td>" +
                "<td>" + data[i]['text'] + "</td>" +
                "</tr>")
            }
        }
    })
    e.preventDefault();
});