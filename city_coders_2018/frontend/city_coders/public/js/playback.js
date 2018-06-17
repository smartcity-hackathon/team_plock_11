L.MoveableCircleMarker = L.Circle.extend({
    initialize: function (latlng, radius, options) {
        L.Circle.prototype.initialize.call(this, latlng, radius, options);
        this.small_circle = null;
        if('double' in options) {
            options.opacity = 0;
            options.fillOpacity = 0.1;
            this.small_circle = new L.Circle(latlng, radius/2, options);
        }
    },

    getPopupContent: function() {
        return this.getRadius();
    },

    move: function (latlng, radius) {
        if(map.hasLayer(this)) {
            this.bringToFront();
        }
        this.setLatLng(latlng);
        this.setRadius(radius);
        if(this.small_circle) {
            if(map.hasLayer(this.small_circle))
                this.small_circle.bringToFront();
            this.small_circle.setLatLng(latlng);
            this.small_circle.setRadius(radius / 2);
        }
    },

    onAdd: function(map_) {
        if(this.small_circle)
            this.small_circle.addTo(map_);
        L.Circle.prototype.onAdd.call(this, map_);
    },

    onRemove: function(map_) {
        if(this.small_circle)
            this.small_circle.removeFrom(map_);
        L.Circle.prototype.onRemove.call(this, map_);
    }
});

L.moveableCircleMarker = function(latlng, radius, options) {
    return new L.MoveableCircleMarker(latlng, radius, options);
};
