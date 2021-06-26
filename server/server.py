# sample from https://github.com/openlawlibrary/pygls
# will be adapted
import asyncio
import json
import time
import uuid
from json import JSONDecodeError
from typing import Optional

from pygls.lsp.methods import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                               TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN)
from pygls.lsp.types import (CompletionItem, CompletionList, CompletionOptions,
                             CompletionParams, ConfigurationItem,
                             ConfigurationParams, Diagnostic,
                             DidChangeTextDocumentParams,
                             DidCloseTextDocumentParams,
                             DidOpenTextDocumentParams, MessageType, Position,
                             Range, Registration, RegistrationParams,
                             Unregistration, UnregistrationParams)
from pygls.lsp.types.basic_structures import (WorkDoneProgressBegin,
                                              WorkDoneProgressEnd,
                                              WorkDoneProgressReport)
from pygls.server import LanguageServer, Server

from .transformer import Transformer

COUNT_DOWN_START_IN_SECONDS = 10
COUNT_DOWN_SLEEP_IN_SECONDS = 1


class TTRLanguageServer(LanguageServer):
    # CMD_COUNT_DOWN_BLOCKING = 'countDownBlocking'
    # CMD_COUNT_DOWN_NON_BLOCKING = 'countDownNonBlocking'
    # CMD_PROGRESS = 'progress'
    # CMD_REGISTER_COMPLETIONS = 'registerCompletions'
    # CMD_SHOW_CONFIGURATION_ASYNC = 'showConfigurationAsync'
    # CMD_SHOW_CONFIGURATION_CALLBACK = 'showConfigurationCallback'
    # CMD_SHOW_CONFIGURATION_THREAD = 'showConfigurationThread'
    # CMD_UNREGISTER_COMPLETIONS = 'unregisterCompletions'

    # CONFIGURATION_SECTION = 'ttrServer'

    def __init__(self):
        super().__init__()


ttr_server = TTRLanguageServer()
transfomer = Transformer()

# TODO: strict typing

# TODO: fix issue with extension debuging and client crash on closing


@ttr_server.thread()
def _transform_to_xml(ls, params):
    ttr_server.show_message("Kicking off transformation...")
    text_doc = ls.workspace.get_document(params.text_document.uri)
    source = text_doc.source
    # TODO: add locking mechanism
    # TODO: add setting for cadence (also on save instead of life reload; delay in seconds)
    out = transfomer.transform(source)
    ttr_server.show_message(out)
    # TODO: store result in output file
    # TODO: add settings for where to store the file
    # TODO: do something with the XML file (xslt?)


def _validate(ls, params):
    ls.show_message_log('Validating ttr...')

    text_doc = ls.workspace.get_document(params.text_document.uri)

    source = text_doc.source
    diagnostics = _validate_ttr(source) if source else []

    ls.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_ttr(source):
    """Validates ttr file."""
    # TODO: make async?
    diagnostics = []

    # TODO: implement validation

    # try:
    #     json.loads(source)
    # except JSONDecodeError as err:
    #     msg = err.msg
    #     col = err.colno
    #     line = err.lineno

    #     d = Diagnostic(
    #         range=Range(
    #             start=Position(line=line - 1, character=col - 1),
    #             end=Position(line=line - 1, character=col)
    #         ),
    #         message=msg,
    #         source=type(ttr_server).__name__
    #     )

    #     diagnostics.append(d)

    return diagnostics


@ttr_server.feature(COMPLETION, CompletionOptions(trigger_characters=[',']))
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""
    # TODO: add standard completions
    # TODO: add completions based on file content
    return CompletionList(
        is_incomplete=False,
        items=[
            # CompletionItem(label='"'),
            # CompletionItem(label='['),
            # CompletionItem(label=']'),
            # CompletionItem(label='{'),
            # CompletionItem(label='}'),
            # CompletionItem(label='$'),
        ]
    )


# @ttr_server.command(TTRLanguageServer.CMD_COUNT_DOWN_BLOCKING)
# def count_down_10_seconds_blocking(ls, *args):
#     """Starts counting down and showing message synchronously.
#     It will `block` the main thread, which can be tested by trying to show
#     completion items.
#     """
#     for i in range(COUNT_DOWN_START_IN_SECONDS):
#         ls.show_message(f'Counting down... {COUNT_DOWN_START_IN_SECONDS - i}')
#         time.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


# @ttr_server.command(TTRLanguageServer.CMD_COUNT_DOWN_NON_BLOCKING)
# async def count_down_10_seconds_non_blocking(ls, *args):
#     """Starts counting down and showing message asynchronously.
#     It won't `block` the main thread, which can be tested by trying to show
#     completion items.
#     """
#     for i in range(COUNT_DOWN_START_IN_SECONDS):
#         ls.show_message(f'Counting down... {COUNT_DOWN_START_IN_SECONDS - i}')
#         await asyncio.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


@ttr_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate(ls, params)
    _transform_to_xml(ls, params)


@ttr_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: TTRLanguageServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message('Text Document Did Close')
    # QUESTION: anything to do here?


@ttr_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message('Text Document Did Open')
    _validate(ls, params)
    _transform_to_xml(ls, params)


# @ttr_server.command(TTRLanguageServer.CMD_PROGRESS)
# async def progress(ls: TTRLanguageServer, *args):
#     """Create and start the progress on the client."""
#     token = 'token'
#     # Create
#     await ls.progress.create_async(token)
#     # Begin
#     ls.progress.begin(token, WorkDoneProgressBegin(title='Indexing', percentage=0))
#     # Report
#     for i in range(1, 10):
#         ls.progress.report(
#             token,
#             WorkDoneProgressReport(message=f'{i * 10}%', percentage=i * 10),
#         )
#         await asyncio.sleep(2)
#     # End
#     ls.progress.end(token, WorkDoneProgressEnd(message='Finished'))
# QUESTION: do I want to use progress for time consuming operations?


# @ttr_server.command(TTRLanguageServer.CMD_REGISTER_COMPLETIONS)
# async def register_completions(ls: TTRLanguageServer, *args):
#     """Register completions method on the client."""
#     params = RegistrationParams(registrations=[
#         Registration(
#             id=str(uuid.uuid4()),
#             method=COMPLETION,
#             register_options={"triggerCharacters": "[':']"})
#     ])
#     response = await ls.register_capability_async(params)
#     if response is None:
#         ls.show_message('Successfully registered completions method')
#     else:
#         ls.show_message('Error happened during completions registration.',
#                         MessageType.Error)
# QUESTION: useful?


# @ttr_server.command(TTRLanguageServer.CMD_SHOW_CONFIGURATION_ASYNC)
# async def show_configuration_async(ls: TTRLanguageServer, *args):
#     """Gets exampleConfiguration from the client settings using coroutines."""
#     try:
#         config = await ls.get_configuration_async(
#             ConfigurationParams(items=[
#                 ConfigurationItem(
#                     scope_uri='',
#                     section=TTRLanguageServer.CONFIGURATION_SECTION)
#             ]))

#         example_config = config[0].get('exampleConfiguration')

#         ls.show_message(f'jsonServer.exampleConfiguration value: {example_config}')

#     except Exception as e:
#         ls.show_message_log(f'Error ocurred: {e}')
# QUESTION: useful?


# @ttr_server.command(TTRLanguageServer.CMD_SHOW_CONFIGURATION_CALLBACK)
# def show_configuration_callback(ls: TTRLanguageServer, *args):
#     """Gets exampleConfiguration from the client settings using callback."""
#     def _config_callback(config):
#         try:
#             example_config = config[0].get('exampleConfiguration')

#             ls.show_message(f'jsonServer.exampleConfiguration value: {example_config}')

#         except Exception as e:
#             ls.show_message_log(f'Error ocurred: {e}')

#     ls.get_configuration(ConfigurationParams(items=[
#         ConfigurationItem(
#             scope_uri='',
#             section=TTRLanguageServer.CONFIGURATION_SECTION)
#     ]), _config_callback)
# QUESTION: useful?


# @ttr_server.thread()
# @ttr_server.command(TTRLanguageServer.CMD_SHOW_CONFIGURATION_THREAD)
# def show_configuration_thread(ls: TTRLanguageServer, *args):
#     """Gets exampleConfiguration from the client settings using thread pool."""
#     try:
#         config = ls.get_configuration(ConfigurationParams(items=[
#             ConfigurationItem(
#                 scope_uri='',
#                 section=TTRLanguageServer.CONFIGURATION_SECTION)
#         ])).result(2)

#         example_config = config[0].get('exampleConfiguration')

#         ls.show_message(f'jsonServer.exampleConfiguration value: {example_config}')

#     except Exception as e:
#         ls.show_message_log(f'Error ocurred: {e}')
# QUESTION: useful?


# @ttr_server.command(TTRLanguageServer.CMD_UNREGISTER_COMPLETIONS)
# async def unregister_completions(ls: TTRLanguageServer, *args):
#     """Unregister completions method on the client."""
#     params = UnregistrationParams(unregisterations=[
#         Unregistration(id=str(uuid.uuid4()), method=COMPLETION)
#     ])
#     response = await ls.unregister_capability_async(params)
#     if response is None:
#         ls.show_message('Successfully unregistered completions method')
#     else:
#         ls.show_message('Error happened during completions unregistration.',
#                         MessageType.Error)
