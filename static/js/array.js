(function($) {
	Array.prototype.indexOf = function(val) {
		for(var i = 0; i < this.length; i++) {
			if(this[i] == val) return i;
		}
		return -1;
	};
	Array.prototype.remove = function(dx) {
		if(isNaN(dx) || dx > this.length) {
			return false;
		}
		for(var i = 0, n = 0; i < this.length; i++) {
			if(this[i] != this[dx]) {
				this[n++] = this[i];
			}
		}
		if(this.length>0)
			this.length -= 1;
	}
})($);