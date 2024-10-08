## Melee
To attack with a [Melee Weapon](Melee) you must be in attack range of your target, unless otherwise specified this is 1m. You may move up to your [[Movement Speed]] in meters as part of your attack to get into Attack Range.

To perform the attack, roll 2d6 and add your [CTR](Control.md) and your Attack bonus, then subtract the targets [[Defense]] from the result. If the result is positive (not 0) the attack hits. This positive result is called the Attack Strength. If the Attack Strength is 10 or more you also land a [[Critical Hit]]
## Damage
Each weapon has its damage given as `<Base> + <Bonus>`. The Base damage is capped by the Attack Strength i.e. the lower of the two numbers is used. The Bonus Damage is always applied as long as the Attack hits at all.
### Examples
A weapon with  5+2 Damage would deal the following damage:

| Strength | Hit  | Base applied | Bonus applied | Damage dealt |
| -------- | ---- | ------------ | ------------- | ------------ |
| 10       | Crit | 5            | 2             | 7            |
| 5        | Yes  | 5            | 2             | 7            |
| 1        | Yes  | 1            | 2             | 3            |
| 0        | No   | 0            | 0             | 0            |
| -3       | No   | 0            | 0             | 0            |
