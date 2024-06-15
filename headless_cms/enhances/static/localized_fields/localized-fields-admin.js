(function($) {
    var syncTabs = function(lang) {
        $('.localized-fields-widget.tab label:contains("'+lang+'")').each(function(){
            $(this).parents('.localized-fields-widget[role="tabs"]').find('.localized-fields-widget.tab').removeClass('active');
            $(this).parents('.localized-fields-widget.tab').addClass('active');
            $(this).parents('.localized-fields-widget[role="tabs"]').children('.localized-fields-widget>[role="tabpanel"]').hide();
            $('#'+$(this).attr('for')).show();

            function handle(i, obj){
                var mainMartor = $(obj);
                var editorId = 'martor-' + mainMartor.data('field-name');
                var editor = ace.edit(editorId);
                var currentTextVal = $(handle.focus_text_area_id).find('textarea').val()

                editor.setValue(currentTextVal)
            }
            handle.focus_text_area_id = '#'+$(this).attr('for')

            $(this).parents('.localized-fields-widget[role="tabs"]').find('.main-martor').each(handle)
        });
    }

    $(window).on("load", function () {
        $('.localized-fields-widget[role="tabs"]').each(function () {
            function handle_martor_edit(i, obj){
                var mainMartor = $(obj);
                var field_name = mainMartor.data('field-name');
                var editorId = 'martor-' + field_name;
                var editor = ace.edit(editorId);
                editor.on('change', function (evt){
                    if (editor.curOp && editor.curOp.command.name){
                        var value = editor.getValue();
                        var curText = mainMartor.parents(
                            '.localized-fields-widget[role="tabs"]'
                        ).find('.localized-panel').not('[style*="display: none"]').find('textarea')
                        curText.val(value)
                    }
                })
            }

            $(this).find('.main-martor').each(handle_martor_edit)
        });


        $('.localized-fields-widget.tab label').click(function(event) {
            event.preventDefault();
            syncTabs(this.innerText);
            if (window.sessionStorage) {
                window.sessionStorage.setItem('localized-field-lang', this.innerText);
            }
            return false;
        });

        if (window.sessionStorage) {
            var lang = window.sessionStorage.getItem('localized-field-lang');

            if (lang) {
                syncTabs(lang);
                return
            }
        }
        $('.localized-fields-widget>[role="tabpanel"]').hide();

        $('.localized-fields-widget[role="tabs"]').each(function () {
            var label = $(this).find('.localized-fields-widget.tab:first label').text();
            syncTabs(label)
        });

    });

})(django.jQuery)
