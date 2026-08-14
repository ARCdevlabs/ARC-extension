"""Revit failures handler."""
from pyrevit import HOST_APP, DOCS, DB
from pyrevit import framework
from pyrevit import coreutils

#pylint: disable=W0703,C0302,C0103

# order is important. ordered from least destructive to most
# the resolver checks whether each one of these resolution types is
# applicable to the failure and applies if applicable

RESOLUTION_TYPES = [DB.FailureResolutionType.MoveElements,
                    DB.FailureResolutionType.CreateElements,
                    DB.FailureResolutionType.DetachElements,
                    DB.FailureResolutionType.FixElements,
                    DB.FailureResolutionType.UnlockConstraints,
                    DB.FailureResolutionType.SkipElements,
                    DB.FailureResolutionType.DeleteElements,
                    DB.FailureResolutionType.QuitEditMode,
                    DB.FailureResolutionType.SetValue,
                    DB.FailureResolutionType.SaveDocument]


# see FailureProcessingResult docs
# http://www.revitapidocs.com/2018.1/f147e6e6-4b2e-d61c-df9b-8b8e5ebe3fcb.htm
# explains usage of FailureProcessingResult options
class FailureSwallower(DB.IFailuresPreprocessor):
    """Swallows all failures."""
    def __init__(self, log_errors=True):
        self._logerror = log_errors
        self._failures_swallowed = []

    def _set_and_resolve(self, failuresAccessor, failure, res_type):
        failure_id = failure.GetFailureDefinitionId()
        # mark as swallowed
        try:
            failure.SetCurrentResolutionType(res_type)
            failuresAccessor.ResolveFailure(failure)
            # mlogger.debug('swallowed: %s', failure_guid)
            self._failures_swallowed.append(failure_id)
        except Exception as frex:
            pass


    def get_swallowed_failures(self):
        failures = set()
        failure_reg = HOST_APP.app.GetFailureDefinitionRegistry()
        if failure_reg:
            for failure_id in self._failures_swallowed:
                failure_obj = failure_reg.FindFailureDefinition(failure_id)
                if failure_obj:
                    failures.add(failure_obj)
        return failures

    def reset(self):
        """Reset swallowed errors."""
        self._failures_swallowed = []

    def preprocess_failures(self, failure_accessor):
        """Pythonic wrapper for `PreprocessFailures` interface method."""
        return self.PreprocessFailures(failure_accessor)

    def PreprocessFailures(self, failuresAccessor):
        """Required IFailuresPreprocessor interface method."""
        severity = failuresAccessor.GetSeverity()

        if severity == coreutils.get_enum_none(DB.FailureSeverity):

            return DB.FailureProcessingResult.Continue

        # log the failure messages
        failures = failuresAccessor.GetFailureMessages()

        # go through failures and attempt resolution
        action_taken = False
        for failure in failures:

            failure_id = failure.GetFailureDefinitionId()
            failure_severity = failure.GetSeverity()
            failure_has_res = failure.HasResolutions()
          
            if not failure_has_res \
                    and failure_severity == DB.FailureSeverity.Warning:
                failuresAccessor.DeleteWarning(failure)
                continue

            # find failure definition id
            # at this point the failure_has_res is True
            failure_def_accessor = get_failure_by_id(failure_id)
            default_res = failure_def_accessor.GetDefaultResolutionType()

            # iterate through resolution options, pick one and resolve
            for res_type in RESOLUTION_TYPES:
                if default_res == res_type:
                    self._set_and_resolve(failuresAccessor, failure, res_type)
                    action_taken = True
                    break
                elif failure.HasResolutionOfType(res_type):
                    self._set_and_resolve(failuresAccessor, failure, res_type)
                    action_taken = True
                    break

        if action_taken:
            return DB.FailureProcessingResult.ProceedWithCommit
        else:
            return DB.FailureProcessingResult.Continue


def get_failure_by_guid(failure_guid):
    fdr = HOST_APP.app.GetFailureDefinitionRegistry()
    fgid = framework.Guid(failure_guid)
    fid = DB.FailureDefinitionId(fgid)
    return fdr.FindFailureDefinition(fid)


def get_failure_by_id(failure_id):
    fdr = HOST_APP.app.GetFailureDefinitionRegistry()
    return fdr.FindFailureDefinition(failure_id)


DEFAULT_TRANSACTION_NAME = 'ARC addin Transaction'


class Transaction():
    """Simplifies transactions by applying ``Transaction.Start()`` and
    ``Transaction.Commit()`` before and after the context.
    Automatically rolls back if exception is raised.

    >>> with Transaction('Move Wall'):
    >>>     wall.DoSomething()

    >>> with Transaction('Move Wall') as action:
    >>>     wall.DoSomething()
    >>>     assert action.status == ActionStatus.Started  # True
    >>> assert action.status == ActionStatus.Committed    # True
    """
    def __init__(self, name=None,
                 doc=None,
                 clear_after_rollback=False,
                 show_error_dialog=False,
                 swallow_errors=False,
                 nested=False):
        doc = doc or DOCS.doc
        # create nested transaction if one is already open
        if doc.IsModifiable or nested:
            self._rvtxn = \
                DB.SubTransaction(doc)
        else:
            self._rvtxn = \
                DB.Transaction(doc, name if name else DEFAULT_TRANSACTION_NAME)
            self._fhndlr_ops = self._rvtxn.GetFailureHandlingOptions()
            self._fhndlr_ops = \
                self._fhndlr_ops.SetClearAfterRollback(clear_after_rollback)
            self._fhndlr_ops = \
                self._fhndlr_ops.SetForcedModalHandling(show_error_dialog)
            if swallow_errors:
                self._fhndlr_ops = \
                    self._fhndlr_ops.SetFailuresPreprocessor(
                        FailureSwallower()
                        )
            self._rvtxn.SetFailureHandlingOptions(self._fhndlr_ops)

    def __enter__(self):
        self._rvtxn.Start()
        return self

    def __exit__(self, exception, exception_value, traceback):
        if exception:
            self._rvtxn.RollBack()
        else:
            try:
                self._rvtxn.Commit()
            except Exception as errmsg:
                pass

    @property
    def name(self):
        if hasattr(self._rvtxn, 'GetName'):
            return self._rvtxn.GetName()

    @name.setter
    def name(self, new_name):
        if hasattr(self._rvtxn, 'SetName'):
            return self._rvtxn.SetName(new_name)

    @property
    def status(self):
        return self._rvtxn.GetStatus()

    def has_started(self):
        return self._rvtxn.HasStarted()

    def has_ended(self):
        return self._rvtxn.HasEnded()

