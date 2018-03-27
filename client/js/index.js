let ractive = Ractive({
	target: "#output",
	template: "#main",
	data: {
		records: [],
		smoke: 0,
	}
})

let clear_log = x => {
	console.log(x);
	return x;
}

ractive.on({
	"addElement" : () => 
		ractive.set("showHelp", true)
			.then(() => ractive.animate("smoke", 1, {duration: 200}))
			.then(() => fetch("/add"))
			.then(() => ractive.animate("smoke", 0, {duration: 200}))
			.then(() => ractive.set("showHelp", false))
			.then(update),
	"emulateMe": (dunno, id) =>
		ractive.set("showEmu", true)
			.then(() => ractive.animate("smoke", 1, {duration: 200}))
			.then(() => fetch(`/emu/${id}`)),
	"cancelEmu": () =>
		fetch("/cancel")
			.then(() => ractive.animate("smoke", 0, {duration: 200}))
			.then(() => ractive.set("showEmu", false))
	
})

let update = () =>
	fetch("/data")
		.then(body => body.json())
		.then(clear_log)
		.then(objs => ractive.set({records: objs}))

update()
