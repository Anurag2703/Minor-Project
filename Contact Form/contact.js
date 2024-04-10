function sendEmail(){
    Email.send({
        Host : "smtp25.elasticemail.com",
        Username : "anuragpanda61@gmail.com",
        Password : "1400055DE9D7E8D1EC001BDDFFB08AE32F1C",
        To : 'anuragpanda2704@gmail.com',
        From : "anuragpanda61@gmail.com",
        Subject : "New Contact Form Enquiry",
        Body : "First Name: " + document.getElementById("first").value
            + "<br> Last Name: " + document.getElementById("last").value 
            + "<br> Email: " + document.getElementById("email").value
            + "<br> Phone no: " + document.getElementById("mobile").value
            + "<br> Message: " + document.getElementById("message").value
    }).then(
        message => alert("Message Sent Successfully")
    );
}