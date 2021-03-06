//
// Created by David Li on 7/17/17.
//

#ifndef ENVIRONMENT_CONSTANTS_HPP
#define ENVIRONMENT_CONSTANTS_HPP

namespace hlt {
    constexpr auto MAX_PLAYERS = 4;
    constexpr auto MAX_QUEUED_MOVES = 1;

    /**
     * Gameplay constants that may be tweaked (though they should be at their
     * default values in a tournament setting).
     */
    struct GameConstants {
        int PLANETS_PER_PLAYER = 8;
        unsigned int EXTRA_PLANETS = 4;

        double DRAG = 2.0;
        double MAX_SPEED = 15.0;
        double MAX_ACCELERATION = 5.0;

        double SHIP_RADIUS = 0.5;

        unsigned short MAX_SHIP_HEALTH = 255;
        unsigned short BASE_SHIP_HEALTH = 255;
        unsigned short DOCKED_SHIP_REGENERATION = 0;

        unsigned int WEAPON_COOLDOWN = 1;
        double WEAPON_RADIUS = 5.0;
        int WEAPON_DAMAGE = 48;
        double EXPLOSION_RADIUS = 5;

        double DOCK_RADIUS = 4;
        unsigned int DOCK_TURNS = 5;
        int RESOURCES_PER_RADIUS = 144;
        int PRODUCTION_PER_SHIP = 72;
        unsigned int BASE_PRODUCTIVITY = 8;
        unsigned int ADDITIONAL_PRODUCTIVITY = 6;

        int SPAWN_RADIUS = 2;

        static auto get_mut() -> GameConstants& {
            // Guaranteed initialized only once by C++11
            static GameConstants instance;
            return instance;
        }

        static auto get() -> const GameConstants& {
            return get_mut();
        }
    };
}

#endif //ENVIRONMENT_CONSTANTS_HPP
