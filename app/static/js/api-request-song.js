const body = document.getElementsByTagName('body')[0];

async function requestSong(song_id){
	const response = await fetch(`/api/song/${song_id}`);
	const data = response.json();

	return data;
}
