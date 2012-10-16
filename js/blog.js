$(document).ready( function (){
   $(".btn-vote_up").click( function() {
      
      var entry_id = $(this).parent().parent().attr("id");
      var v = $(this).parent().children("strong")[0];
      var current_votes = v.innerHTML;

      $.ajax({
          url: "/blog/votes",
          type: "GET",
          data: {votes: current_votes, sign: "plus", entry: entry_id},
          dataType: "text",
          success: function(result){
            $(v).html(result); 
          }      
     }); 
   });
});


$(document).ready( function (){
   $(".btn-vote_down").click( function() {
      
      var entry_id = $(this).parent().parent().attr("id");
      var v = $(this).parent().children("strong")[0];
      var current_votes = v.innerHTML;
      $.ajax({
          url: "/blog/votes",
          type: "GET",
          data: {votes: current_votes, sign: "minus", entry: entry_id},
          dataType: "text",
          success: function(result){
            $(v).html(result); 
          }      
     }); 
   });
});
