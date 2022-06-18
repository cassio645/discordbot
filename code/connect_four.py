import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from functools import partial
from db.mydb import insert_c4_winner, add_money

import emojis


number_emojis = {
    1: "\u0031\ufe0f\u20e3",
    2: "\u0032\ufe0f\u20e3",
    3: "\u0033\ufe0f\u20e3",
    4: "\u0034\ufe0f\u20e3",
    5: "\u0035\ufe0f\u20e3",
    6: "\u0036\ufe0f\u20e3",
    7: "\u0037\ufe0f\u20e3",
    8: "\u0038\ufe0f\u20e3",
    9: "\u0039\ufe0f\u20e3"
}
NUMBERS = list(number_emojis.values())

class Game:
    """A Connect 4 Game."""

    def __init__(
        self,
        bot,
        channel,
        player1,
        player2,
        tokens,
        size
    ):
        self.bot = bot
        self.channel = channel
        self.player1 = player1
        self.player2 = player2 or AI(self.bot, game=self)
        self.tokens = tokens

        self.grid = self.generate_board(size)
        self.grid_size = size

        self.unicode_numbers = NUMBERS[:self.grid_size]

        self.message = None

        self.player_active = None
        self.player_inactive = None

    @staticmethod
    def generate_board(size: int):
        """Generate the connect 4 board."""
        return [[0 for _ in range(7)] for _ in range(7)]

    async def print_grid(self) -> None:
        """Formats and outputs the Connect Four grid to the channel."""
        title = (
            f"Connect 4\n {self.player1.display_name}"
            f" VS {self.bot.user.display_name if isinstance(self.player2, AI) else self.player2.display_name}"
        )

        rows = [" ".join(self.tokens[s] for s in row) for row in self.grid]
        first_row = " ".join(x for x in NUMBERS[:self.grid_size])
        formatted_grid = "\n".join([first_row] + rows)
        embed = discord.Embed(title=title, description=formatted_grid)


        if self.message:
            await self.message.edit(embed=embed)
        else:
            self.message = await self.channel.send(content="Carregando...")
            for emoji in self.unicode_numbers:
                await self.message.add_reaction(emoji)
            await self.message.edit(content=None, embed=embed)

    async def game_over(self, action: str, player1: discord.user, player2: discord.user) -> None:
        """Announces to public chat."""
        if action == "win":
            if player2.bot or player1.bot:
                if player2.bot:
                    money = randint(20, 60)
                    add_money(player1.id, money)
                await self.channel.send(f"Game Over! {player1.mention} venceu {player2.mention}.")
            else:
                insert_c4_winner(player1.id)
                await self.channel.send(f"Game Over! {player1.mention} venceu {player2.mention}")
        elif action == "draw":
            await self.channel.send(f"Game Over! {player1.mention} e {player2.mention} Empataram")
        await self.print_grid()

    async def start_game(self) -> None:
        """Begins the game."""
        self.player_active, self.player_inactive = self.player1, self.player2

        while True:
            await self.print_grid()

            if isinstance(self.player_active, AI):
                coords = self.player_active.play()
                if not coords:
                    await self.game_over(
                        "draw",
                        self.bot.user if isinstance(self.player_active, AI) else self.player_active,
                        self.bot.user if isinstance(self.player_inactive, AI) else self.player_inactive,
                    )
            else:
                coords = await self.player_turn()

            if not coords:
                return

            if self.check_win(coords, 1 if self.player_active == self.player1 else 2):
                await self.game_over(
                    "win",
                    self.bot.user if isinstance(self.player_active, AI) else self.player_active,
                    self.bot.user if isinstance(self.player_inactive, AI) else self.player_inactive,
                )
                return

            self.player_active, self.player_inactive = self.player_inactive, self.player_active

    def predicate(self, reaction: discord.Reaction, user: discord.Member) -> bool:
        """The predicate to check for the player's reaction."""
        return (
            reaction.message.id == self.message.id
            and user.id == self.player_active.id
            and str(reaction.emoji) in (*self.unicode_numbers, "\u274C")
        )

    async def player_turn(self):
        """Initiate the player's turn."""
        message = await self.channel.send(
            f"Sua vez {self.player_active.mention}"
        )
        player_num = 1 if self.player_active == self.player1 else 2
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=self.predicate, timeout=120.0)
            except asyncio.TimeoutError:
                if self.player_inactive.id:
                    insert_c4_winner(self.player_inactive.id)
                await self.channel.send(f"{self.player_active.mention}, demorou demais... Game over!")
                return
            else:
                await message.delete()


                await self.message.remove_reaction(reaction, user)

                column_num = self.unicode_numbers.index(str(reaction.emoji))
                column = [row[column_num] for row in self.grid]

                for row_num, square in reversed(list(enumerate(column))):
                    if not square:
                        self.grid[row_num][column_num] = player_num
                        return row_num, column_num
                message = await self.channel.send(f"A coluna {column_num + 1} já está cheia...")

    def check_win(self, coords, player_num: int) -> bool:
        """Check that placing a counter here would cause the player to win."""
        vertical = [(-1, 0), (1, 0)]
        horizontal = [(0, 1), (0, -1)]
        forward_diag = [(-1, 1), (1, -1)]
        backward_diag = [(-1, -1), (1, 1)]
        axes = [vertical, horizontal, forward_diag, backward_diag]

        for axis in axes:
            counters_in_a_row = 1  # The initial counter that is compared to
            for (row_incr, column_incr) in axis:
                row, column = coords
                row += row_incr
                column += column_incr

                while 0 <= row < self.grid_size and 0 <= column < self.grid_size:
                    if self.grid[row][column] == player_num:
                        counters_in_a_row += 1
                        row += row_incr
                        column += column_incr
                    else:
                        break
            if counters_in_a_row >= 4:
                return True
        return False


class AI:
    """The Computer Player for Single-Player games."""

    def __init__(self, bot, game: Game):
        self.game = game
        self.mention = bot.user.mention

    def get_possible_places(self):
        """Gets all the coordinates where the AI could possibly place a counter."""
        possible_coords = []
        for column_num in range(self.game.grid_size):
            column = [row[column_num] for row in self.game.grid]
            for row_num, square in reversed(list(enumerate(column))):
                if not square:
                    possible_coords.append((row_num, column_num))
                    break
        return possible_coords

    def check_ai_win(self, coord_list):
        """
        Check AI win.
        Check if placing a counter in any possible coordinate would cause the AI to win
        with 10% chance of not winning and returning None
        """
        if random.randint(1, 10) == 1:
            return
        for coords in coord_list:
            if self.game.check_win(coords, 2):
                return coords

    def check_player_win(self, coord_list):
        """
        Check Player win.
        Check if placing a counter in possible coordinates would stop the player
        from winning with 25% of not blocking them  and returning None.
        """
        if random.randint(1, 4) == 1:
            return
        for coords in coord_list:
            if self.game.check_win(coords, 1):
                return coords

    @staticmethod
    def random_coords(coord_list):
        """Picks a random coordinate from the possible ones."""
        return random.choice(coord_list)

    def play(self):
        """
        Plays for the AI.
        Gets all possible coords, and determins the move:
        1. coords where it can win.
        2. coords where the player can win.
        3. Random coord
        The first possible value is choosen.
        """
        possible_coords = self.get_possible_places()

        if not possible_coords:
            return False

        coords = (
            self.check_ai_win(possible_coords)
            or self.check_player_win(possible_coords)
            or self.random_coords(possible_coords)
        )

        row, column = coords
        self.game.grid[row][column] = 2
        return coords


class ConnectFour(commands.Cog):
    """Connect Four. The Classic Vertical Four-in-a-row Game!"""

    def __init__(self, bot):
        self.bot = bot
        self.games: list[Game] = []
        self.waiting: list[discord.Member] = []
        #self.channels = [985991485876998207, 985989056502562886, 985962497364328499]
        self.channels = [968045281843220520, 968048613806723082, 982711181259210833, 983428734692503652, 981554796358152202]

        self.tokens = [":white_circle:", ":blue_circle:", ":red_circle:"]

        self.max_board_size = 7
        self.min_board_size = 7

    async def check_author(self, ctx: commands.Context) -> bool:
        """Check if the requester is free and the board size is correct."""
        if self.already_playing(ctx.author):
            await ctx.send("Você já está jogando!")
            return False

        if ctx.author in self.waiting:
            await ctx.send("Você já enviou um pedido para o Jogador 2")
            return False

        return True

    def get_player(
        self,
        ctx: commands.Context,
        announcement: discord.Message,
        reaction: discord.Reaction,
        user: discord.Member
    ) -> bool:
        """Predicate checking the criteria for the announcement message."""
        if self.already_playing(ctx.author):  # If they've joined a game since requesting a player 2
            return True  # Is dealt with later on

        if (
            user.id not in (ctx.me.id, ctx.author.id)
            and str(reaction.emoji) == "🤚"
            and reaction.message.id == announcement.id
        ):
            if self.already_playing(user):
                self.bot.loop.create_task(ctx.send(f"{user.mention} Você já está jogando!"))
                self.bot.loop.create_task(announcement.remove_reaction(reaction, user))
                return False

            if user in self.waiting:
                self.bot.loop.create_task(ctx.send(
                    f"{user.mention} Você ainda está em uma partida ativa."
                ))
                self.bot.loop.create_task(announcement.remove_reaction(reaction, user))
                return False

            return True

        if (
            user.id == ctx.author.id
            and str(reaction.emoji) == "\u274C"
            and reaction.message.id == announcement.id
        ):
            return True
        return False

    def already_playing(self, player: discord.Member) -> bool:
        """Check if someone is already in a game."""
        return any(player in (game.player1, game.player2) for game in self.games)

    @staticmethod
    def check_emojis(
        e1, e2
    ):
        """Validate the emojis, the user put."""
        if isinstance(e1, str) and emojis.count(e1) != 1:
            return False, e1
        if isinstance(e2, str) and emojis.count(e2) != 1:
            return False, e2
        return True, None

    async def _play_game(
        self,
        ctx,
        user,
        emoji1: str,
        emoji2: str
    ) -> None:
        """Helper for playing a game of connect four."""
        self.tokens = [":white_circle:", "\U0001f535", "\U0001f534"]
        game = None  # if game fails to intialize in try...except

        try:
            game = Game(self.bot, ctx.channel, ctx.author, user, self.tokens, size=7)
            self.games.append(game)
            await game.start_game()
            self.games.remove(game)
        except Exception:
            # End the game in the event of an unforeseen error so the players aren't stuck in a game
            await ctx.send(f"{ctx.author.mention} {user.mention if user else ''} Aconteceu um erro. Game Over!")
            if game in self.games:
                self.games.remove(game)
            raise

    @commands.group(
        invoke_without_command=True,
        aliases=("4inarow", "connect4", "connectfour", "c4"),
        case_insensitive=True
    )
    async def connect_four(
        self,
        ctx: commands.Context,
        emoji1 = "\U0001f535",
        emoji2 = "\U0001f534"
    ) -> None:
        if int(ctx.channel.id) not in self.channels:
            await ctx.send("Esse comando não é permitido aqui. Use em <#983428734692503652>")
            return None
        """
        Play the classic game of Connect Four with someone!
        Sets up a message waiting for someone else to react and play along.
        The game will start once someone has reacted.
        All inputs will be through reactions.
        """
        check, emoji = self.check_emojis(emoji1, emoji2)


        check_author_result = await self.check_author(ctx)
        if not check_author_result:
            return

        announcement = await ctx.send(
            "**Connect Four**: Um novo jogo está iniciando!\n"
            f"Clique em 🤚 para jogar com {ctx.author.mention}!\n"
            f"(Cancela a partida '\u274C'.)"
        )
        self.waiting.append(ctx.author)
        await announcement.add_reaction("🤚")
        await announcement.add_reaction("\u274C")

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=partial(self.get_player, ctx, announcement),
                timeout=60.0
            )
        except asyncio.TimeoutError:
            self.waiting.remove(ctx.author)
            await announcement.delete()
            await ctx.send(
                f"{ctx.author.mention} Parece que não há ninguém aqui para jogar. "
                f"Use `{ctx.prefix}{ctx.invoked_with} ia` para jogar contra a Inteligencia Artificial."
            )
            return

        if str(reaction.emoji) == "\u274C":
            self.waiting.remove(ctx.author)
            await announcement.delete()
            await ctx.send(f"{ctx.author.mention} Partida cancelada.")
            return

        await announcement.delete()
        self.waiting.remove(ctx.author)
        if self.already_playing(ctx.author):
            return

        await self._play_game(ctx, user, str(emoji1), str(emoji2))

    @connect_four.command(aliases=("bot", "ia", "cpu"))
    async def ai(
        self,
        ctx: commands.Context,
        emoji1 = "\U0001f535",
        emoji2 = "\U0001f534"
    ) -> None:
        """Play Connect Four against a computer player."""

        check_author_result = await self.check_author(ctx)
        if not check_author_result:
            return

        await self._play_game(ctx, None, str(emoji1), str(emoji2))


def setup(bot):
    """Load ConnectFour Cog."""
    bot.add_cog(ConnectFour(bot))