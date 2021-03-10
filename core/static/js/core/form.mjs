/**
 * Prevent submit using enter key
 * 
 * @param form The form element
 */
export function preventEnter(form) {
    $(form).on('keypress', function(e) {
        if ($(e.target).attr('type') === 'submit') {
            return true;
        }

        // Allow newlines in textareas
        if (e.target instanceof HTMLTextAreaElement) {
            e.stopPropagation();
            return true;
        }
        
        if (e.which === 13) { //&& !fieldsArePopulated(form)) {
            return false;
        }
    });
}
