const spotifyUrlInput = document.getElementById("input-url");
const wrongInputMessage = document.getElementById("wrong-input-message");

const spotifyIdLength = 22;

function animatePromise(domObject, keyframeParams, animationParams){
	return new Promise((resolve) => {
		const animation = domObject.animate(keyframeParams, animationParams);
		animation.onfinish = () => resolve(domObject);
	});
}

async function animateFadingElement(element){
	if(element.isAnimated === true) return;
	element.isAnimated = true;
	await animatePromise(element,
		[
		{
			opacity: 1,
		},
		{
			opacity: 0.5,
		}
		],
		{
			duration: 200,
			fill: "forwards",
			transitionTimingFunction : 'ease-in-out',
		}
	);
	await animatePromise(element,
		[
		{
			opacity: 0.5,
		},
		{
			opacity: 1,
		}
		],
		{
			duration: 200,
			fill: "forwards",
			transitionTimingFunction : 'ease-in-out',
		}
	);
	element.isAnimated = false;
}

function invalidInput(message){
	wrongInputMessage.innerHTML = message;
	if(wrongInputMessage.style.opacity == 0){
		wrongInputMessage.style.opacity = 1;
	}
	else{
		animateFadingElement(wrongInputMessage);
	}

}

async function submitForm(){
	if(spotifyUrlInput.value.length === 0) return;

	var parser = document.createElement('a');
	parser.href = spotifyUrlInput.value;

	try{
		if(!parser.hostname.includes("spotify")) throw new Error();
		var song_id = parser.pathname.split('/')[2];
		if(song_id.length != spotifyIdLength){
			throw new Error();
		}
	}
	catch(error){
		invalidInput("Spotify url is not correct")
		return false;
	}

	window.location.href = `/song/${song_id}`
}
