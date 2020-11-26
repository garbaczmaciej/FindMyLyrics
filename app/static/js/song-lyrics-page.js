const mainSection = document.getElementsByClassName("big-section")[0];
const informationSection = document.getElementsByClassName("information-section")[0];


function animatePromise(domObject, keyframeParams, animationParams){
	return new Promise((resolve) => {
		const animation = domObject.animate(keyframeParams, animationParams);
		animation.onfinish = () => resolve(domObject);
	});
}

function createNode(nodeType, nodeValue='', nodeId=undefined, nodeClasses=undefined){
	const node = document.createElement(nodeType);
	node.innerHTML = nodeValue;

	if(nodeId !== undefined) node.id = nodeId;
	if(nodeClasses !== undefined){
		if(typeof nodeClasses !== Array) node.classList.add(nodeClasses);
		else {
			nodeClasses.forEaach(className => {
				node.classList.add(className);
			});
		}
	}

	return node;
}

async function createErrorSection(errorData){
}

async function createSongSection(songData){
	const songSection = createNode('section', '', '', "song-section");

	const leftSection = createNode('div', '', 'left-section');
	const rightSection = createNode('section', '', 'right-section');


	const albumImage = createNode("img", '', 'album-image');
	albumImage.src = songData.album.images[0].url;
	leftSection.appendChild(albumImage);

	leftSection.appendChild(createNode('h1', songData.name, "song-name"));
	leftSection.appendChild(createNode('h2', songData.artists.join(', '), "song-artists"));

	const lyricsWrapper = createNode('div', '', 'lyrics-wrapper');
	lyricsWrapper.appendChild(createNode('p', songData.lyrics, "song-lyrics"));
	rightSection.appendChild(lyricsWrapper);

	songSection.appendChild(leftSection);
	songSection.appendChild(rightSection);

	mainSection.style.height = 'auto';

	mainSection.appendChild(songSection);
}

async function getSongFromApi(song_id){
	const songData = await requestSong(song_id);
	await animatePromise(informationSection,
		[{opacity:1}, {opacity:0}],
		{duration: 400, fill:"forwards"}
	);

	if(songData.error === true){
		createErrorSection(songData);
	}
	else{
		informationSection.style.display = 'none';
		createSongSection(songData);
	}
}
