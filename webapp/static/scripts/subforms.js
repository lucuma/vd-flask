/*!
 * SubForms.js
*
 * A collection of functions to work with subforms and python's
 * library “Solution”
 *
 * Copyright 2014 Juan-Pablo Scaletti
 * Released under the MIT license
 *
 * Date: 2014-05-17
 */
window.EVENT_SUBFORM_ADD = 'subform.add';
window.EVENT_SUBFORM_DEL = 'subform.del';

function parseHTML(html){
    html = $.trim(html);
    if ($.parseHTML){
        html = $.parseHTML(html)[0];
    }
    return $(html);
}


function initSubForms($wrapper){
    $wrapper.find('[data-forms]').each(function(){
        initSubForm($(this));
    });
}
initSubForms($(document));


function initSubForm($w){
    var delmsg = $w.attr('data-delmsg');

    var $btnAdd = $w.next('[data-addbtn]');
    $btnAdd = $btnAdd.length ? $btnAdd : $w.next().find('[data-addbtn]');

    var tmplSel = $btnAdd.attr('data-addbtn');

    $btnAdd
        .off('click')  // deactivate any action set by a possible parent form
        .on('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            addSubForm($w, tmplSel);
        });

    $w.on('click', '[data-delbtn]', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var $f = $(this).closest('[data-form]');
        if (!delmsg || $f.prop('data-new') || confirm(delmsg)){
            removeSubForm($w, $f);
        }
    });

    toggleSubFormsHeader($w);
}


function addSubForm($w, tmplSel){
    var maxforms = parseInt($w.attr('data-maxforms'), 10);
    if (!isNaN(maxforms)){
        var $subForms = $w.find('[data-form="' + $w.attr('data-forms') + '"]');
        if ($subForms.length >= maxforms){
            return;
        }
    }

    var html = $(tmplSel).html();
    var $pre = parseHTML(html);
    $pre.prop('data-new', true);
    $pre.hide().appendTo($w).slideDown('fast');
    updateSubFormsNames($w);

    $w.trigger(EVENT_SUBFORM_ADD, $pre);

    // Recursive subforms
    initSubForm($pre.find('[data-forms]'));
    return $pre;
}


function removeSubForm($w, $f){
    $f.find('[data-delbtn]').hide();
    $f.slideUp('fast', function(){
        $f.remove();
        $w.trigger(EVENT_SUBFORM_DEL, $f);
        updateSubFormsNames($w);
    });
}


function toggleSubFormsHeader($w){
    var $forms = $w.find('[data-form]');
    if ($forms.length){
        $w.find('.subform-header').show();
    } else {
        $w.find('.subform-header').hide();
    }
}


function updateSubFormsNames($w){
    var name, newName, $fw, $subForms, depth, i, j;

    toggleSubFormsHeader($w);
    var aa = $w.toArray();
    var bb = $w.parents('[data-forms]').toArray();
    var $wrappers = $(bb.concat(aa));

    for (i=$wrappers.length; i>0; i--){
        depth = i - 1;
        $fw = $wrappers.eq(depth);
        $subForms = $fw.find('[data-form="' + $fw.attr('data-forms') + '"]');

        for (j=0; j<$subForms.length; j++){
            var num = j + 1;
            updateNames($subForms.eq(j), depth, num);
        }
    }
}


function updateNames($form, depth, num){
    var $fields = $form.find('[name]');
    var $field, oldName, newName, nameParts;

    $fields.each(function(){
        $field = $(this);
        oldName = $field.attr('name');
        nameParts = deconstructName(oldName);
        newName = getNewName(nameParts, depth, num);
        $field.attr('name', newName);
    });
}


function deconstructName(name){
    var nameParts = [];
    var parts = name.split('-');
    var maxIndex = parts.length - 1;
    var i = 0, subpart;

    for (i=0; subpart=parts[i]; i++) {
        if (i > 0){
            subpart = '-' + subpart;
        }
        if (i == maxIndex){
            nameParts.push(subpart);
            continue;
        }
        subpart = subpart.split('.');
        nameParts.push(subpart[0] + '.');
        nameParts.push(subpart[1]);
    }
    return nameParts;
}


function getNewName(nameParts, depth, num){
    nameParts[depth * 2 + 1] = num;
    return nameParts.join('');
}
