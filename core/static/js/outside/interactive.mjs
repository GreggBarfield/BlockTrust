import {attach as contactUsAttach} from './contact_us.mjs';

$(function(){
    /**
     * Contact Us forms
     */
    $("#interactive-contact-us").each(function () {
        contactUsAttach(this);
    });
});
