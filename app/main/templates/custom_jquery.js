
<script type="text/javascript">
            $(function (){
                $('a#active_item').click(function() {
                    var active_item = this.name;
                    console.log(active_item);
                    $.ajax({
                        type : 'POST',
                        url : "{{url_for('refresh_inbox')}}",
                        data : {'active_item': active_item},
                        success : function(data) {
                            $("#messages_active").html(data);
                            },
                        error: function(XMLHttpRequest, textStatus, errorThrown) {
                            alert(XMLHttpRequest, textStatus, errorThrown)
                        }
                        });
                });
            });
        </script>

<script type="text/javascript">
            $(document).ready(function(){
                $('lkl').click(function() {
                    var active_id = this.getAttributeNode("data-id").value;
                    $.ajax({
                        type : 'POST',
                        url : "{{url_for('message_profile')}}",
                        data : {'active_item': active_id},
                        async : false,
                        success : function(data) {
                            $("#active_message_profile").html(data);
                            },
                        error: function(XMLHttpRequest, textStatus, errorThrown) {
                            alert(XMLHttpRequest, textStatus, errorThrown)
                            }
                     });

                 });
            });
         </script>

