const heartIcons = document.querySelectorAll('.heart-icon');
const likeCounts = document.querySelectorAll('.like-count');
console.log(likeCounts.innerText);
heartIcons.forEach(icon => {

    icon.addEventListener('click', function() {
    
        const slug = this.dataset.slug;

        const isLiked = this.classList.contains('fa-thumbs-up');
        console.log(isLiked)
        console.log(JSON.stringify({ 'slug': slug }));
        fetch(path+"?slug="+slug )
        .then(response => response.json())
        .then(data => {
            if (data.success){
                if (isLiked) {
                    this.classList.remove('fa-thumbs-up');
                    this.classList.add('fa-thumbs-down');
                    window.location.href = cur_path;
                } else {
                    this.classList.remove('fa-thumbs-down');
                    this.classList.add('fa-thumbs-up');
                    window.location.href = cur_path;
                }
                
                    // count.innerText = data.likes;
            
                console.log(data.items);
            } else {
                if(data.message==='redirect'){
                    window.location.href ='http://127.0.0.1:8000/accounts/login/';
                }else{
                alert(data.message);
                }
            }
        })
        .catch(error =>  {
            console.log(error)
        })
    
    });


});
