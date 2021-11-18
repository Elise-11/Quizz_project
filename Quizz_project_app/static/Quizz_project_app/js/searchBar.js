$(document).ready(function(){

    $(".quizz").css({'left': '22%'});
    $("select[name='listbox']").css({'position': 'absolute', 'top': '39.3%', 'left': '23%', 'width': '10%', 'height': '3.2%'});
    $("input[name='searchBar']").css({'position': 'absolute', 'top': '39.3%', 'left': '33%', 'width': '35%'});
    $("option[value='']").attr('style', 'display:none;');
    $(".ui-autocomplete").css({ 'height': '25%', 'overflow-y': 'scroll', 'overflow-x': 'hidden', 'width': '20%'});
    $("button[type='submit']").css({'position': 'absolute', 'top': '39.3%', 'left': '68%', 'width': '7%', 'height': '3.2%'});
});